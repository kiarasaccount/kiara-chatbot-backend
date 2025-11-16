from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# Allow your GitHub Pages site to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # You can restrict later
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class Question(BaseModel):
    question: str

# Your custom FAQ answers
FAQ = {
    "when is the best time to contact you": 
        "Monday - Friday between 9-5.",
    "what is the best way to contact you": 
        "Please contact me via email kiara0441@gmail.com, I would love to set up a call!",
    "how long has kiara been coding for": 
        "Kiara has been coding for 4 years now! She would be a great addition to your team!",
}

def check_faq(user_q: str):
    q = user_q.lower().strip()
    for key in FAQ:
        if key in q:
            return FAQ[key]
    return None


@app.post("/ask")
async def ask(question: Question):
    user_q = question.question

    # 1️⃣ Check if it's a known FAQ question
    faq_answer = check_faq(user_q)
    if faq_answer:
        return {"answer": faq_answer}

    # 2️⃣ Otherwise, ask OpenAI
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": "You are Kiara, a friendly helpful assistant on her portfolio website."},
                {"role": "user", "content": user_q}
            ]
        )

        ai_answer = completion.choices[0].message["content"]
        return {"answer": ai_answer}

    except Exception as e:
        print("Error:", e)
        return {"answer": "Sorry, something went wrong. Please try again!"}
