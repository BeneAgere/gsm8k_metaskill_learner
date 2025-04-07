from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

chat_completion_model = "gpt-4o"

def create_open_ai_client():
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )

    client = AzureOpenAIChatCompletionClient(
        azure_deployment="gpt-4o",
        model=chat_completion_model,
        api_version="2024-02-01",
        azure_endpoint="https://devpythiaaoaieus.openai.azure.com/",
        azure_ad_token_provider=token_provider,
    )
    return client

def create_embedding_client():
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )

    endpoint = "https://secphio1.openai.azure.com/"
    deployment = "text-embedding-3-small"

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider=token_provider,
        api_version="2023-09-01-preview"
    )

    return client
