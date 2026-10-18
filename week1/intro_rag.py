import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv("./workspace/.env", override=True)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-120b"

knowledge_base = {
    "age": "The age of Pratyush is 25 years.",
    "networth": "The networth of Pratyush is 2000 rupees."
}

def retrieve_info(question: str) -> str:
    """A rigid software function that matches keywords."""
    question = question.lower()
    
    if "age" in question:
        return knowledge_base["age"]
    elif "networth" in question:
        return knowledge_base["networth"]
    else:
        return "None"
    
def ask_llm(question:str):
    context = retrieve_info(question)
    
    system_prompt = f"""
    Answer in one line only.
    Answer ONLY based on this context. Do not hallucinate.
    Context: {context}
    """
    
    messages= [
        {
            "role": "system", "content": system_prompt
        },
        {"role": "user", "content": question}
    ]
    
    response = client.chat.completions.create(model=MODEL, messages= messages, temperature=0)
    return response.choices[0].message.content

print("--- Works well ---")
print("Q: What is Pratyush's age?")
print("A:", ask_llm("What is Pratyush's age?"))
print()

print("Q: What is Pratyush's networth?")
print("A:", ask_llm("What is Pratyush's networth?"))
    