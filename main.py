from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Allow your GitHub website
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Question(BaseModel):
    question: str


# --- Your custom Q&A knowledge ---
FAQ = {
    "when is the best time to contact you": 
        "Monday - Friday between 9–5.",
    
    "what is the best way to contact you": 
        "Please contact me via email: kiara0441@gmail.com — I’d love to set up a call!",
    
    "how long has kiara been coding": 
        "Kiara has been coding for 4 years now! She would be a great addition to your team!"
}

def check_faq(user_question: str):
    q = user_question.lower()

    for key, value in FAQ.items():
        if key in q:
            return value
    return None


@app.post("/ask")
async def ask_model(question: Question):

    # 1. Check your custom FAQ first
    faq_answer = check_faq(question.question)
    if faq_answer:
        return {"answer": faq_answer}

    # 2. Fall back to GPT model for everything else
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=question.question
        )

        answer = response.output_text

        return {"answer": answer}

    except Exception as e:
        return {"answer": f"Error: {str(e)}"}

