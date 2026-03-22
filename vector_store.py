import json
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

class VectorStore:
    def __init__(self, data_paths: List[str]):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents = []
        self._load_documents(data_paths)

    def _load_documents(self, paths: List[str]):
        for path in paths:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    text = f"{item.get('specialty', '')} {item.get('category', '')} {item['content']}"
                    embedding = self.model.encode(text).tolist()
                    self.documents.append({
                        'text': item['content'],
                        'metadata': {k: v for k, v in item.items() if k != 'content'},
                        'embedding': embedding
                    })
        print(f"Loaded {len(self.documents)} document chunks.")

    def _cosine_similarity(self, emb1, emb2):
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

    def search(self, query: str, top_k: int = 3, threshold: float = 0.3) -> List[Dict[str, Any]]:
        query_emb = self.model.encode(query).tolist()
        scored = []
        for doc in self.documents:
            sim = self._cosine_similarity(query_emb, doc['embedding'])
            scored.append((sim, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        filtered = [doc for sim, doc in scored if sim >= threshold]

        if any(kw in query.lower() for kw in ['chest', 'heart', 'cardiac', 'angina']):
            filtered = [doc for doc in filtered if doc['metadata'].get('specialty') != 'dental']

        return filtered[:top_k]