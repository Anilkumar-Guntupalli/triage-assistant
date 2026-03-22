# 🚑 Real-Time Emergency Triage Assistant

A voice‑enabled, low‑latency triage assistant designed for emergency rooms and disaster zones.  
It intelligently prunes irrelevant patient history (e.g., dental records when a cardiac event is suspected) and delivers step‑by‑step recommendations in under 500ms.

---

## Features

- Intelligent Context Pruning – Only relevant medical history and protocols are used.  
- Ultra‑Low Latency – Average response time <500ms, displayed live.  
- Voice Input – Hands‑free operation using the Web Speech API.  
- Professional UI – Modern, responsive layout with authentic medical imagery.  
- Demo Examples – One‑click test cases to showcase pruning.  

---

## Tech Stack

- Backend: FastAPI, Groq (LLM), Sentence‑Transformers (embeddings), Python‑dotenv  
- Frontend: HTML, Tailwind CSS, Font Awesome, Web Speech API  
- Vector Store: Custom in‑memory similarity search with cosine similarity  

---

## Getting Started

### 1. Clone the repository

git clone https://github.com/yourusername/triage-assistant.git
cd triage-assistant

### 2. Create a virtual environment and install dependencies

python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt

### 3. Set up your Groq API key

Create a .env file in the root directory with:

GROQ_API_KEY=your_key_here

(Get a free key at console.groq.com)

### 4. Run the backend server

uvicorn main:app --host 0.0.0.0 --port 8000

### 5. Open the frontend

Double‑click index.html in your browser (Chrome recommended for voice).

### 6. Test it

- Type: "65-year-old male with chest pain and history of hypertension"  
- Click Ask – see the pruned context and recommendation.  
- Try voice input or the example buttons.

---

## How It Works

1. Query – User speaks or types an emergency description.  
2. Retrieval – Embeddings are computed and compared to stored patient records and protocols.  
3. Pruning – Only documents above a similarity threshold are kept; additional keyword filters remove irrelevant categories (e.g., dental records for cardiac queries).  
4. LLM Call – A concise recommendation is generated using Groq’s llama-3.1-8b-instant.  
5. Display – Results show the recommendation, the context used, and what was ignored (noise reduction). Latency is displayed in milliseconds.

---

## Project Context

This project was built as part of an HPE Internship application.  
The challenge: create a real‑time triage assistant that can analyse a large repository of patient history and disaster protocols in under 500ms while ignoring irrelevant data.

---

## Screenshots

<img width="1898" height="896" alt="Screenshot 2026-03-22 211021" src="https://github.com/user-attachments/assets/285aa7f8-7490-4f48-a751-382ccef25bd3" />
<img width="1899" height="910" alt="Screenshot 2026-03-22 211051" src="https://github.com/user-attachments/assets/9bdf7150-1413-44fe-9c5e-10d9e770fa4c" />
<img width="1900" height="902" alt="Screenshot 2026-03-22 211141" src="https://github.com/user-attachments/assets/e8deeb60-b094-42fe-9032-3f5cc2310a34" />

---

## License

MIT
