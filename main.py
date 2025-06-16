from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

OLLAMA_API = "http://localhost:11434/api/chat"
model = "llama3.2"

system_prompt = (
    "You are a health assistant. "
    "Only answer questions related to health, fitness, medicine, mental wellness, or nutrition."
    "If a question is not related to health, reply: 'Sorry, I can only answer health-related questions.'"
)

# system_prompt = (
#     "You are a mathematics assistant. "
#     "Only answer questions related to mathematics. "
#     "If a question is not about math, reply: 'Sorry, I can only answer math-related questions.'"
# )

class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat(message: ChatMessage):
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message.message}
        ]
        
        response = requests.post(
            OLLAMA_API,
            json={
                "model": model,
                "messages": messages,
                "stream": False
            }
        )
        
        reply = response.json()['message']['content']
        return {"response": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 