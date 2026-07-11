from azure.ai.projects import AIProjectClient
from azure.identity import InteractiveBrowserCredential
import json

FOUNDRY_PROJECT_ENDPOINT = "https://turismoia.services.ai.azure.com/api/projects/agencia-turismo"

project = AIProjectClient(
    endpoint=FOUNDRY_PROJECT_ENDPOINT,
    credential=InteractiveBrowserCredential(redirect_uri="http://localhost:8080"),
)
openai_client = project.get_openai_client()

ferramentas = [
    {
        "type": "function",
        "name": "buscar_previsao_tempo",
        "description": "Busca a previsão do tempo (temperatura e chance de chuva) para uma coordenada geográfica e data específica.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number", "description": "Latitude do local"},
                "longitude": {"type": "number", "description": "Longitude do local"},
                "data": {"type": "string", "description": "Data no formato YYYY-MM-DD"},
            },
            "required": ["latitude", "longitude", "data"],
        },
    }
]

pergunta = "Vou pra Cancún no dia 15/07/2026. Como vai estar o tempo? (coordenadas: lat 21.16, lon -86.85)"

response = openai_client.responses.create(
    model="gpt-4o",
    input=pergunta,
    tools=ferramentas,
)

for item in response.output:
    print("---")
    print(item)