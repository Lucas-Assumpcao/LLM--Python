from sentence_transformers import SentenceTransformer, util

# Baixa um modelo pequeno e leve na primeira execução (depois fica em cache)
modelo = SentenceTransformer('all-MiniLM-L6-v2')

palavras = ["rei", "rainha", "banana", "monarca"]

# Gera o embedding (vetor) de cada palavra
embeddings = modelo.encode(palavras)

print(f"Tamanho do vetor de 'rei': {len(embeddings[0])} números")
print()

# Compara a similaridade entre pares de palavras
for i in range(len(palavras)):
    for j in range(i + 1, len(palavras)):
        similaridade = util.cos_sim(embeddings[i], embeddings[j])
        print(f"{palavras[i]} <-> {palavras[j]}: {similaridade.item():.3f}")