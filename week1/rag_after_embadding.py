import os
import sys
import numpy as np
from groq import Groq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv("/workspace/.env", override=True)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "openai/gpt-oss-120b"

print("Loading embedding model...")
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

documents = [
    "Employees receive 24 days of paid leave per year.",
    "Employees can work from home 3 days a week.",
    "The company provides 3000 rupees per month for internet.",
    "Health insurance is provided to all full-time employees.",
    "The annual performance review happens in December.",
    "Employees get a free gym membership."
]

# This returns a numpy array of shape (6, 384)
print("Embedding documents...")

doc_embeddings = embed_model.encode(documents)
# print(doc_embeddings)

def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_a = np.linalg.norm(v1)
    norm_b = np.linalg.norm(v2)
    return dot_product / (norm_a * norm_b)

def retrieve(query, query_embeddings):
    scores = []
    for i, doc_embedding in enumerate(doc_embeddings):
        score = cosine_similarity(query_embedding, doc_embedding)
        scores.append((score, documents[i]))
        
    scores.sort(key=lambda x: x[0], reverse=True)
    
    return scores[0]

def ask_llm(query, context):
    system_prompt = f"""
    Answer the user's question in one line.
    Answer ONLY based on the context provided below. Do not hallucinate.
    If the context doesn't contain the answer, say "I don't know".
    
    Context: {context}
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]
    
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content


user_query = "How much vacation do I get?"
print(f"\nUser Query: {user_query}")

query_embedding = embed_model.encode(user_query)
top_score, top_context = retrieve(user_query, query_embedding)

print(f"Top Match Score: {top_score:.4f}")
print(f"Retrieved Context: {top_context}")

answer = ask_llm(user_query, top_context)
print(f"\nLLM Answer: {answer}")



