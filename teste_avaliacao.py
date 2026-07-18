import re
import time
import json
from sentence_transformers import SentenceTransformer, util
from azure.ai.projects import AIProjectClient
from azure.identity import InteractiveBrowserCredential

FOUNDRY_PROJECT_ENDPOINT = "https://turismoia.services.ai.azure.com/api/projects/agencia-turismo"

# --- Preparação do RAG (igual à Fase 4) ---
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

project = AIProjectClient(
    endpoint=FOUNDRY_PROJECT_ENDPOINT,
    credential=InteractiveBrowserCredential(redirect_uri="http://localhost:8080"),
)
openai_client = project.get_openai_client()

def responder_com_rag(pergunta: str) -> tuple[str, float]:
    """Retorna (resposta, tempo_gasto_em_segundos)"""
    inicio = time.time()
    
    chunks_relevantes = buscar_chunks_relevantes(pergunta, top_k=3)
    contexto = "\n\n---\n\n".join(chunks_relevantes)
    
    prompt = f"""Responda a pergunta do usuário usando APENAS as informações do contexto abaixo.
Se o contexto não tiver a resposta, diga que não encontrou essa informação no documento.

Contexto:
{contexto}

Pergunta: {pergunta}"""
    
    response = openai_client.responses.create(model="gpt-4.1-mini", input=prompt)
    
    resposta_texto = ""
    for item in response.output:
        if item.type == "message":
            for block in item.content:
                if hasattr(block, "text"):
                    resposta_texto += block.text
    
    tempo_gasto = time.time() - inicio
    return resposta_texto, tempo_gasto

def julgar_resposta(pergunta: str, resposta_real: str, criterio: str) -> bool:
    """LLM-as-a-judge: avalia se a resposta atende ao critério"""
    prompt_juiz = f"""Você é um avaliador rigoroso. Compare a resposta dada com o critério esperado.

Pergunta: {pergunta}
Resposta dada: {resposta_real}
Critério esperado: {criterio}

A resposta atende ao critério? Responda APENAS "SIM" ou "NÃO" (sem mais nada)."""
    
    response = openai_client.responses.create(model="gpt-4.1-mini", input=prompt_juiz)
    
    veredito = ""
    for item in response.output:
        if item.type == "message":
            for block in item.content:
                if hasattr(block, "text"):
                    veredito += block.text
    
    return "SIM" in veredito.upper()

# --- Golden Dataset ---
golden_dataset = [
    {
        "pergunta": "O que é tool calling?",
        "criterio": "A resposta deve explicar que o modelo decide qual função chamar e o código do desenvolvedor executa essa função.",
    },
    {
        "pergunta": "Quantas fases tem o roadmap?",
        "criterio": "A resposta deve mencionar que são 7 fases (0 a 6).",
    },
    {
        "pergunta": "O roadmap fala sobre receitas de culinária italiana?",
        "criterio": "A resposta deve dizer que essa informação não está no documento/contexto.",
    },
]

# --- Rodando a avaliação ---
print("=" * 60)
resultados = []

for caso in golden_dataset:
    resposta, tempo = responder_com_rag(caso["pergunta"])
    passou = julgar_resposta(caso["pergunta"], resposta, caso["criterio"])
    
    resultados.append({
        "pergunta": caso["pergunta"],
        "passou": passou,
        "tempo": tempo,
    })
    
    status = "✅ PASSOU" if passou else "❌ FALHOU"
    print(f"\n{status} | {tempo:.2f}s")
    print(f"Pergunta: {caso['pergunta']}")
    print(f"Resposta: {resposta[:150]}...")

# --- Resumo final ---
total = len(resultados)
passaram = sum(1 for r in resultados if r["passou"])
tempo_medio = sum(r["tempo"] for r in resultados) / total

print("\n" + "=" * 60)
print(f"RESUMO: {passaram}/{total} testes passaram")
print(f"Tempo médio por resposta: {tempo_medio:.2f}s")