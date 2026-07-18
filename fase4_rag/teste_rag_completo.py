import re
from sentence_transformers import SentenceTransformer, util
from azure.ai.projects import AIProjectClient
from azure.identity import InteractiveBrowserCredential

FOUNDRY_PROJECT_ENDPOINT = "https://turismoia.services.ai.azure.com/api/projects/agencia-turismo"

# --- Preparação (chunking + embeddings) ---
with open("roadmap-llm-python.md", "r", encoding="utf-8") as f:
    conteudo = f.read()

chunks = re.split(r"(?=^## )", conteudo, flags=re.MULTILINE)
chunks = [c.strip() for c in chunks if c.strip()]

modelo_embeddings = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embeddings_chunks = modelo_embeddings.encode(chunks)

def buscar_chunks_relevantes(pergunta: str, top_k: int = 3) -> list[str]:
    embedding_pergunta = modelo_embeddings.encode(pergunta)
    similaridades = util.cos_sim(embedding_pergunta, embeddings_chunks)[0]
    indices_ordenados = similaridades.argsort(descending=True)[:top_k]
    return [chunks[idx] for idx in indices_ordenados]

# --- Retrieval ---
pergunta = "O que eu preciso aprender sobre chamar funções externas com o modelo?"
chunks_relevantes = buscar_chunks_relevantes(pergunta, top_k=3)

contexto = "\n\n---\n\n".join(chunks_relevantes)

# --- Geração aumentada ---
project = AIProjectClient(
    endpoint=FOUNDRY_PROJECT_ENDPOINT,
    credential=InteractiveBrowserCredential(redirect_uri="http://localhost:8080"),
)
openai_client = project.get_openai_client()

prompt = f"""Responda a pergunta do usuário usando APENAS as informações do contexto abaixo.
Se o contexto não tiver a resposta, diga que não encontrou essa informação no documento.

Contexto:
{contexto}

Pergunta: {pergunta}"""

response = openai_client.responses.create(
    model="gpt-4.1-mini",
    input=prompt,
)

for item in response.output:
    if item.type == "message":
        for block in item.content:
            if hasattr(block, "text"):
                print(block.text)