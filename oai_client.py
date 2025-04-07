from autogen_ext.models.openai import AzureOpenAIChatCompletionClient, OpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI, OpenAI

chat_completion_model = "gpt-4o"
embedding_model = "text-embedding-3-small"

def create_open_ai_client(aad_auth):
    if aad_auth:
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
    else:
        client = OpenAIChatCompletionClient(
            model=chat_completion_model, temperature=0.3
        )  # assuming OPENAI_API_KEY is set in the environment.
        return client


def create_embedding_client(aad_auth=False):
    if aad_auth:
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
        )

        endpoint = "https://secphio1.openai.azure.com/"
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
            api_version="2023-09-01-preview"
        )
    else:
        client = OpenAI() # assuming OPENAI_API_KEY is set in the environment.
        return client

    return client
