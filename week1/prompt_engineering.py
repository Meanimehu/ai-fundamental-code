import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv("/workspace/.env", override=True)

api_key = os.getenv("GROQ_API_KEY")
if not api_key or api_key == "your_groq_api_key_here":
    raise ValueError("Set a valid GROQ_API_KEY in /workspace/.env")

client = Groq(api_key=api_key)
MODEL = "openai/gpt-oss-120b"

def ask_llm(prompt: str) -> str:
    """Send a prompt to the LLM and return the raw answer string."""
    messages = [
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content


bad_prompt = """
This is a user complaint. My laptop is not working. Classify this.
"""

good_prompt = """
ROLE:
You are a customer support assistant at a laptop company.

TASK:
You have to classify the customer's issue into one category.

CONSTRAINTS:
The category must be exactly one of: billing, technical, return.
No other categories exist. Do not invent new categories.

OUTPUT FORMAT:
Answer in ONE WORD ONLY. No punctuation, no explanation, no surrounding text.

EXAMPLES:
- "I want a refund." -> return
- "My laptop won't turn on." -> technical
- "I was charged twice." -> billing

FALLBACK:
If the issue does not fit any of the categories above, answer: other

Now classify this customer message:
"My laptop is not working."
"""

print("=" * 60)
print("BAD PROMPT")
print("=" * 60)
print(ask_llm(bad_prompt))
print()

print("=" * 60)
print("GOOD PROMPT")
print("=" * 60)
print(ask_llm(good_prompt))
print()
    