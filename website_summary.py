import requests
from bs4 import BeautifulSoup

OLLAMA_API = "http://localhost:11434/api/chat"
model = "llama3.2"

def get_website_data(url):
    
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string if soup.title else "No Title Found"
    text = soup.get_text(separator="\n", strip=True)
    return title, text
    

def summarize_website_with_ollama(title, text):
   
    user_prompt_content = (
        f"You are looking at the website titled \"{title}\". "
        "The content of this website is as follows; "
        "please provide a short summary of this website in markdown. "
        "If it includes news or announcements, then summarize these too.\n\n"
        f"\"\"\"\n{text}\n\"\"\"\n\n"
    )

    system_prompt = "You are a helpful assistant that summarizes website content."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_content}
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
    return reply
    

if __name__ == "__main__":

    url = input("Enter the URL : ") # https://www.apple.com/

    title, text = get_website_data(url)

   
    print("title : ",title)
    print("......\n")

    summary = summarize_website_with_ollama(title, text)
    print("Summary:\n", summary)

