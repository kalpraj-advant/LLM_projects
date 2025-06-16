import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyB0wcycFa77q2AR6VYH9Jundai1Zg6MsUU"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-pro")

user_prompt = (
        "Hello"
    )

response = model.generate_content(user_prompt)
print("Response:")
print(response.text)