import requests

OLLAMA_API = "http://localhost:11434/api/chat"

def chat_with_tinyllama(user_input):
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": user_input}
    ]

    response = requests.post(
        OLLAMA_API,
        json={
            "model": "llama3.2",
            "messages": messages,
            "stream": False
        }
    )

    response.raise_for_status()
    reply = response.json()['message']['content']
    return reply

def run_chatbot():
    print("'exit' to quit\n")
    while True:
        user_input = input("You: ")
        if user_input == "exit":
            break

        reply = chat_with_tinyllama(user_input)
        print(f"Bot: {reply}\n")

if __name__ == "__main__":
    run_chatbot()
