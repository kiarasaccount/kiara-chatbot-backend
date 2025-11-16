from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

client = OpenAI()

app = FastAPI()

# Allow your HTML/JS website to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or set your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str

@app.post("/chat")
async def chat(msg: Message):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": msg.text}]
    )
    
    reply = response.choices[0].message["content"]
    return {"reply": reply}
