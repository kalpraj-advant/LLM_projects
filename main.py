from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json

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

ticket_prices = {
    "london": "$799",
    "paris": "$899",
    "tokyo": "$1400",
    "berlin": "$499"
}

flight_times = {
    "london": "10:00 to 18:00",
    "paris": "12:00 to 20:00",
    "tokyo": "20:00 to 04:00",
    "berlin": "06:00 to 14:00"
}


system_prompt = (
    "You are a helpful assistant for an Airline called FlightAI. "
    "Give short, courteous answers, no more than 1 sentence. "
    "Always be accurate. If you don't know the answer, say so. "
    f"Here are the ticket prices: {json.dumps(ticket_prices)}. "
    f"And here are the flight times: {json.dumps(flight_times)}."
)

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
