import re

with open("roadmap-llm-python.md", "r", encoding="utf-8") as f:
    conteudo = f.read()

# Divide o texto sempre que encontrar um título de nível 2 (##), mantendo o título junto do chunk
chunks = re.split(r"(?=^## )", conteudo, flags=re.MULTILINE)

# Remove chunks vazios ou só com espaços
chunks = [c.strip() for c in chunks if c.strip()]

print(f"Total de chunks: {len(chunks)}\n")
for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i} ({len(chunk)} caracteres) ---")
    print(chunk[:150])  # só os primeiros 150 caracteres, pra não poluir a tela
    print()