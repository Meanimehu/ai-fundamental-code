import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv("/workspace/.env", override=True)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

prompt = "Hello"

messages = [
    {"role": "user", "content": prompt}
]

print("Prompt being sent:", prompt)

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=messages
)

print("Answer:", response.choices[0].message.content)
print("Full response:", response)