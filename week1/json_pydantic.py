import os
import json
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv("/workspace/.env", override=True)

api_key = os.getenv("GROQ_API_KEY")

if not api_key or api_key == "your_groq_api_key_here":
    raise ValueError("Set a valid GROQ_API_KEY in /workspace/.env")


client = Groq(api_key=api_key)
MODEL = "openai/gpt-oss-120b"

class Ticket(BaseModel):
    name: str
    email: str
    issue: str
    
schema = Ticket.model_json_schema()

text = """
Hello, my name is Pratyush. I purchased an iPhone from your store
and it stopped working. My address is Delhi. My father's name is
Kumar. I broke up with my girlfriend Sheetal. Please contact me
on abc@gmail.com. Regards, Pratyush. Phone: 82155.
"""

prompt = f"This is a customer ticket. Please extract the personal information from this: {text}"

system_prompt = f"""
Extract the requested information and give me a JSON output.
Strictly follow this schema and nothing else:
{schema}
Do NOT invent information. Do NOT return the schema itself.
If a field is absent, omit it or set it to null.
"""

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user",   "content": prompt},
]

response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    response_format={"type": "json_object"},   # <-- guarantees valid JSON
    temperature=0,
)

raw_json = response.choices[0].message.content
print("RAW JSON from model:\n", raw_json, "\n")

data = json.loads(raw_json)  
ticket = Ticket(**data) 

print("PARSED FIELDS:", ticket, data, raw_json)
print("  name :", ticket.name)
print("  email:", ticket.email)
print("  issue:", ticket.issue)