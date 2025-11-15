# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Kiara Assistant Backend")

# Enable CORS so GitHub Pages frontend can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://kiarasaccount.github.io"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple Pydantic model for request body
class Question(BaseModel):
    question: str

# Retrieval-based QA
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
    },
]

# Helper function to find answer
def get_answer(user_question: str) -> str:
    user_question_lower = user_question.lower()
    for qa in qa_pairs:
        if qa["question"].lower() == user_question_lower:
            return qa["answer"]
    return "Sorry, I don't know the answer to that yet."

# POST endpoint for frontend
@app.post("/ask")
async def ask(question: Question):
    answer = get_answer(question.question)
    return {"answer": answer}

# Optional root endpoint for testing
@app.get("/")
async def root():
    return {"message": "Kiara Assistant Backend is live!"}
