from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

# Load OpenAI API key from Render Environment Variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow your GitHub Pages site to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

# Custom Q&A
CUSTOM_RESPONSES = {
    "when is the best time to contact you": 
        "Monday - Friday between 9-5.",
    
    "what is the best way to contact you": 
        "Please contact me via email kiara0441@gmail.com, I would love to set up a call!",
    
    "how long has kiara been coding for": 
        "Kiara has been coding for 4 years now! She would be a great addition to your team!",
}

def check_custom_answer(user_question: str):
    q_lower = user_question.lower().strip()
    for key, value in CUSTOM_RESPONSES.items():
        if key in q_lower:
            return value
    return None

@app.post("/ask")
async def ask_question(data: Question):
    user_q = data.question

    # 1️⃣ Check custom answers first
    custom = check_custom_answer(user_q)
    if custom:
        return {"answer": custom}

    # 2️⃣ Otherwise fallback to GPT-4o-mini
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Kiara's helpful assistant."},
            {"role": "user", "content": user_q}
        ]
    )

    ai_answer = completion.choices[0].message["content"]
    return {"answer": ai_answer}
