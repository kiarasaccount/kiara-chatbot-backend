from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import numpy as np
from openai import OpenAI
import os

# --------------------------------------------
# CONFIG
# --------------------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
EMBED_MODEL = "text-embedding-3-small"

app = FastAPI()

# --------------------------------------------
# KNOWLEDGE BASE
# --------------------------------------------

qa_pairs = [
    {
        "question": "When is the best time to contact you?",
        "answer": "Monday - Friday between 9-5."
    },
    {
        "question": "What is the best way to contact you?",
        "answer": "Please contact me via email kiara0441@gmail.com, I would love to set up a call!"
    },
    {
        "question": "How long has Kiara been coding for?",
        "answer": "Kiara has been coding for 4 years now! She would be a great addition to your team!"
    }
]

# Embed stored questions once at startup
def embed(text):
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=text
    )
    return np.array(response.data[0].embedding, dtype=float)

stored_embeddings = [embed(item["question"]) for item in qa_pairs]


# --------------------------------------------
# MODEL
# --------------------------------------------

class Query(BaseModel):
    question: str


# Cosine similarity
def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# Retrieval-based answer
def retrieve_answer(user_query):
    user_emb = embed(user_query)

    similarities = [
        cosine_similarity(user_emb, stored_emb)
        for stored_emb in stored_embeddings
    ]

    best_idx = int(np.argmax(similarities))
    return qa_pairs[best_idx]["answer"]


# --------------------------------------------
# ENDPOINT
# --------------------------------------------

@app.post("/ask")
def ask(q: Query):
    answer = retrieve_answer(q.question)
    return {"answer": answer}
