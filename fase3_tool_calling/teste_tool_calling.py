from azure.ai.projects import AIProjectClient
from azure.identity import InteractiveBrowserCredential
import json
import requests

FOUNDRY_PROJECT_ENDPOINT = "https://turismoia.services.ai.azure.com/api/projects/agencia-turismo"

def buscar_previsao_tempo(latitude: float, longitude: float, data: str) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto",
        "start_date": data,
        "end_date": data,
    }
    resposta = requests.get(url, params=params)
    dados = resposta.json()
    return {
        "temp_max": dados["daily"]["temperature_2m_max"][0],
        "temp_min": dados["daily"]["temperature_2m_min"][0],
        "chance_chuva": dados["daily"]["precipitation_probability_max"][0],
    }

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

# 1ª chamada: o modelo decide chamar a ferramenta
response = openai_client.responses.create(
    model="gpt-4.1-mini",
    input=pergunta,
    tools=ferramentas,
)

pedido_funcao = response.output[0]
print("Modelo pediu para chamar:", pedido_funcao.name)
print("Com argumentos:", pedido_funcao.arguments)

# 2. Executa a função de verdade, com os argumentos que o modelo extraiu
argumentos = json.loads(pedido_funcao.arguments)
resultado_real = buscar_previsao_tempo(**argumentos)
print("\nResultado real da API de clima:", resultado_real)

# 3. Devolve o resultado pro modelo, referenciando o call_id
response_final = openai_client.responses.create(
    model="gpt-4.1-mini",
    previous_response_id=response.id,
    input=[
        {
            "type": "function_call_output",
            "call_id": pedido_funcao.call_id,
            "output": json.dumps(resultado_real),
        }
    ],
    tools=ferramentas,
)

# 4. Extrai a resposta final em texto
print("\n--- Resposta final do modelo ---")
for item in response_final.output:
    if item.type == "message":
        for block in item.content:
            if hasattr(block, "text"):
                print(block.text)