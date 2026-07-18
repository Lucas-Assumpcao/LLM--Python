from azure.ai.projects import AIProjectClient
from azure.identity import InteractiveBrowserCredential

FOUNDRY_PROJECT_ENDPOINT = "https://turismoia.services.ai.azure.com/api/projects/agencia-turismo"

project = AIProjectClient(
    endpoint=FOUNDRY_PROJECT_ENDPOINT,
    credential=InteractiveBrowserCredential(redirect_uri="http://localhost:8080"),
)

for deployment in project.deployments.list():
    print(deployment)