from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

system_prompt = (
    "You are a mathematics assistant. "
    "Only answer questions related to mathematics. "
    "If a question is not about math, reply: 'Sorry, I can only answer math-related questions.'"
)

class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat(message: ChatMessage):
    try:
        payload = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 1024,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": message.message}
            ]
        }

        headers = {
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(ANTHROPIC_URL, json=payload, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        reply = response.json()["content"][0]["text"]
        return {"response": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
