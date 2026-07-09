from pydantic import BaseModel

class RequisitosViagem(BaseModel):
    pais: str
    documento_principal: str
    validade_minima: str
    visto_necessario: bool
    detalhes_visto: str

import json
from azure.ai.projects import AIProjectClient
from azure.identity import InteractiveBrowserCredential
from pydantic import BaseModel, ValidationError

FOUNDRY_PROJECT_ENDPOINT = "https://turismoia.services.ai.azure.com/api/projects/agencia-turismo"
AGENT_NAME = "TurismoIA"

class RequisitosViagem(BaseModel):
    pais: str
    documento_principal: str
    validade_minima: str
    visto_necessario: bool
    detalhes_visto: str

project = AIProjectClient(
    endpoint=FOUNDRY_PROJECT_ENDPOINT,
    credential=InteractiveBrowserCredential(redirect_uri="http://localhost:8080"),
)
openai_client = project.get_openai_client()
conversation = openai_client.conversations.create()

prompt = """Responda APENAS com um JSON válido, sem texto antes ou depois, sem markdown, seguindo exatamente este schema:

{
  "pais": string,
  "documento_principal": string,
  "validade_minima": string,
  "visto_necessario": boolean,
  "detalhes_visto": string
}

Pergunta: Quais os requisitos de documentos para viajar para o Canadá?"""

response = openai_client.responses.create(
    input=prompt,
    conversation=conversation.id,
    extra_body={
        "agent_reference": {"type": "agent_reference", "name": AGENT_NAME}
    },
)

texto_resposta = ""
for item in response.output:
    if item.type == "message":
        for block in item.content:
            if hasattr(block, "text"):
                texto_resposta += block.text

print("--- Resposta bruta do modelo ---")
print(texto_resposta)

# Tenta converter e validar
try:
    dados = json.loads(texto_resposta)
    requisitos = RequisitosViagem(**dados)
    print("\n--- Validado com sucesso ---")
    print(requisitos)
    print(f"\nPrecisa de visto? {requisitos.visto_necessario}")
except json.JSONDecodeError:
    print("\nERRO: o modelo não retornou um JSON válido.")
except ValidationError as e:
    print(f"\nERRO de validação Pydantic: {e}")