import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import numpy as np

# Load API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY environment variable")

client = OpenAI(api_key=OPENAI_API_KEY)

EMBED_MODEL = "text-embedding-3-small"

# Your Q&A data
qa_pairs = [
    {"question": "What services do you offer?", "answer": "I offer a variety of services..."},
    {"question": "How can I contact support?", "answer": "You can contact support by..."}
]

# Lazy-loaded embeddings
stored_embeddings = None

def embed(text: str):
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=text
    )
    return np.array(response.data[0].embedding)

def load_embeddings():
    global stored_embeddings
    if stored_embeddings is None:
        stored_embeddings = [embed(item["question"]) for item in qa_pairs]

def find_best_answer(query):
    load_embeddings()

    query_embedding = embed(query)
    similarities = [np.dot(query_embedding, e) for e in stored_embeddings]
    best_idx = int(np.argmax(similarities))
    return qa_pairs[best_idx]["answer"]

# FastAPI app
app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_question(payload: Query):
    answer = find_best_answer(payload.question)
    return {"answer": answer}
