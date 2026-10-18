import os 
from dotenv import load_dotenv
from groq import Groq

load_dotenv("/workspace/.env", override=True)

api_key = os.getenv("GROQ_API_KEY")

if not api_key or api_key == "your_groq_api_key_here":
    raise ValueError("Set a valid GROQ_API_KEY in /workspace/.env")

client = Groq(api_key = api_key)
model = 'openai/gpt-oss-120b'

prompts = [
    "Hi",                                          # tiny prompt, tiny answer
    "Explain time travel in detail.",              # medium prompt, big answer
    "Write a 1000-word essay on machine learning.",# large prompt, huge answer
]

for prompt in prompts:
    messages= [
        {"role": "user", "content": prompt}
    ]
    
    response= client.chat.completions.create(model = model, messages=messages)
    usage = response.usage
    
    print("=" * 60)
    print("PROMPT:", prompt)
    print("-" * 60)
    print("ANSWER:", response.choices[0].message.content)
    print("-" * 60)
    print("prompt_tokens     :", usage.prompt_tokens)
    print("completion_tokens :", usage.completion_tokens)
    print("total_tokens      :", usage.total_tokens)
    print("finish_reason     :", response.choices[0].finish_reason)
    print()
    