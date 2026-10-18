import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading model (this may take a moment the first time)...")
model = SentenceTransformer('all-MiniLM-L6-v2')

text = "Machine learning is fun"
embedding = model.encode(text)

print(f"\nOriginal text: {text}")
print(f"Vector shape: {embedding.shape}")
print(f"First 10 numbers in the vector: {embedding[:10]}")

def cosine_similarity(v1, v2):
    
    dot_product = np.dot(v1, v2)
    norm_a = np.linalg.norm(v1)
    norm_b = np.linalg.norm(v2)
    
    return dot_product / (norm_a * norm_b)

t1 = "There are 24 paid leaves."
t2 = "There are 24 vacation days."
t3 = "I love pizza."

v1 = model.encode(t1)
v2 = model.encode(t2)
v3 = model.encode(t3)

score_1_2 = cosine_similarity(v1, v2)
score_1_3 = cosine_similarity(v1, v3)

print("\n--- Similarity Scores ---")
print(f"Score 1 & 2 ('paid leaves' vs 'vacation days'): {score_1_2:.4f}")
print(f"Score 1 & 3 ('paid leaves' vs 'I love pizza'): {score_1_3:.4f}")