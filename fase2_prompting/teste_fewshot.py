from azure.ai.projects import AIProjectClient
from azure.identity import InteractiveBrowserCredential

FOUNDRY_PROJECT_ENDPOINT = "https://turismoia.services.ai.azure.com/api/projects/agencia-turismo"
AGENT_NAME = "TurismoIA"

project = AIProjectClient(
    endpoint=FOUNDRY_PROJECT_ENDPOINT,
    credential=InteractiveBrowserCredential(redirect_uri="http://localhost:8080"),
)

openai_client = project.get_openai_client()
conversation = openai_client.conversations.create()

prompt_fewshot = """Responda SEMPRE no formato abaixo, sem emojis, sem comentários extras:

Exemplo 1:
Pergunta: Documentos para viajar para o Japão?
Resposta:
- País: Japão
- Documento principal: Passaporte válido
- Validade mínima: 6 meses além da data de retorno
- Visto: Não exigido para turismo até 90 dias (passaporte brasileiro)

Exemplo 2:
Pergunta: Documentos para viajar para os Estados Unidos?
Resposta:
- País: Estados Unidos
- Documento principal: Passaporte válido + visto americano (B1/B2)
- Validade mínima: durante toda a estadia
- Visto: Obrigatório, solicitado com antecedência

Agora responda no mesmo formato:
Pergunta: Documentos para viajar para a Austrália?
Resposta:"""

response = openai_client.responses.create(
    input=prompt_fewshot,
    conversation=conversation.id,
    extra_body={
        "agent_reference": {"type": "agent_reference", "name": AGENT_NAME}
    },
)

for item in response.output:
    if item.type == "message":
        for block in item.content:
            if hasattr(block, "text"):
                print(block.text)