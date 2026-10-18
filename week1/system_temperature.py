import os
from dotenv import load_dotenv
from groq import Groq

# override=True is critical: Docker may have a stale value; this forces the real .env
load_dotenv("/workspace/.env", override=True)

api_key = os.getenv("GROQ_API_KEY")
if not api_key or api_key == "your_groq_api_key_here":
    raise ValueError("Set a valid GROQ_API_KEY in /workspace/.env")

client = Groq(api_key=api_key)
model = "openai/gpt-oss-120b"

# --- SYSTEM ROLE: tells the LLM who it is ---
system_message = {
    "role": "system",
    "content": (
        "You are a brand naming expert. "
        "Suggest exactly one creative name for a food brand."
    ),
}

# --- USER: the actual question ---
user_message = {
    "role": "user",
    "content": "Suggest a name for my new food company.",
}

messages = [system_message, user_message]   # system FIRST, then user

response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0.7,   # try 0, 1, 2 later
)

print("Answer:")
print(response.choices[0].message.content)
print("\nToken usage:")
print(response.usage)