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

response = openai_client.responses.create(
    input="Oi! Quais documentos preciso pra viajar pra Europa?",
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