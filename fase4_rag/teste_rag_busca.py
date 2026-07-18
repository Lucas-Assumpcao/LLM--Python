import re
from sentence_transformers import SentenceTransformer, util

with open("roadmap-llm-python.md", "r", encoding="utf-8") as f:
    conteudo = f.read()

chunks = re.split(r"(?=^## )", conteudo, flags=re.MULTILINE)
chunks = [c.strip() for c in chunks if c.strip()]

modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embeddings_chunks = modelo.encode(chunks)

def buscar_chunks_relevantes(pergunta: str, top_k: int = 2) -> list[str]:
    embedding_pergunta = modelo.encode(pergunta)
    similaridades = util.cos_sim(embedding_pergunta, embeddings_chunks)[0]
    
    # Pega os índices dos top_k chunks mais similares, em ordem decrescente
    indices_ordenados = similaridades.argsort(descending=True)[:top_k]
    
    resultados = []
    for idx in indices_ordenados:
        resultados.append((chunks[idx], similaridades[idx].item()))
    return resultados

# Teste com uma pergunta real sobre o roadmap
pergunta = "O que eu preciso aprender sobre chamar funções externas com o modelo?"
resultados = buscar_chunks_relevantes(pergunta, top_k=2)

for chunk, score in resultados:
    print(f"--- Similaridade: {score:.3f} ---")
    print(chunk[:200])
    print()