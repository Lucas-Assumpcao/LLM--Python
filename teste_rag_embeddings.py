import re
from sentence_transformers import SentenceTransformer

with open("roadmap-llm-python.md", "r", encoding="utf-8") as f:
    conteudo = f.read()

chunks = re.split(r"(?=^## )", conteudo, flags=re.MULTILINE)
chunks = [c.strip() for c in chunks if c.strip()]

# Modelo multilíngue, melhor para português que o testado na Fase 1
modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

embeddings_chunks = modelo.encode(chunks)

print(f"Total de chunks: {len(chunks)}")
print(f"Dimensão de cada embedding: {len(embeddings_chunks[0])}")