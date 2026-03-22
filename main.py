import os
import time
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
from vector_store import VectorStore

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

vector_store = VectorStore([
    "data/patient_records.json",
    "data/disaster_protocols.json"
])

app = FastAPI(title="Triage Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TriageRequest(BaseModel):
    query: str

class TriageResponse(BaseModel):
    recommendation: str
    used_context: list
    latency_ms: float

@app.post("/triage", response_model=TriageResponse)
async def triage(request: TriageRequest):
    start_time = time.time()
    try:
        relevant_docs = vector_store.search(request.query, top_k=3, threshold=0.25)

        if not relevant_docs:
            context_text = "No relevant patient history or protocols found."
            used_context = []
        else:
            context_text = "\n\n".join([doc['text'] for doc in relevant_docs])
            used_context = relevant_docs

        prompt = f"""You are an emergency triage assistant. Based ONLY on the context below, recommend the next best action.

Context:
{context_text}

Current query: {request.query}

Recommendation (be concise, step-by-step):"""

        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",   # <-- FIXED: replaced decommissioned model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=200
        )
        recommendation = completion.choices[0].message.content

        latency_ms = (time.time() - start_time) * 1000
        return TriageResponse(
            recommendation=recommendation,
            used_context=[doc['text'] for doc in used_context],
            latency_ms=round(latency_ms, 2)
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/health")
def health():
    return {"status": "ok"}