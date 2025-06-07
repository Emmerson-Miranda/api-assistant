from openai import OpenAI
from app.core import config
from app.core.openai_embedding_mock import response_from_openai_embedding_api
import logging


logging.basicConfig(level=logging.INFO)

mock = config.get_openai_mock_enable()

if not mock:
    # OpenAI client initialization
    client = OpenAI(api_key=config.get_openai_api_key())


def generate_embedding(text: str, model: str = "text-embedding-3-small"):
    """
    Generate an embedding for the given text using OpenAI's API.
    Args:
        text (str): The input text to generate an embedding for.
        model (str): The model to use for generating the embedding.
    Returns:
        list: The embedding vector for the input text.
    """
    if not text:
        raise ValueError("Input text cannot be empty.")
    if not model:
        raise ValueError("Model cannot be empty.")
    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")
    if not isinstance(model, str):
        raise TypeError("Model must be a string.")
    if len(model) == 0:
        raise ValueError("Model name cannot be empty.")

    logging.info(f"OpenAI embedding API call mock enable: {mock}")

    if mock:
        # https://platform.openai.com/docs/guides/embeddings/embedding-models
        return response_from_openai_embedding_api["data"][0]["embedding"]
    else:
        text = text.replace("\n", " ")
        response = client.embeddings.create(
            input=text,
            model=model
        )
        return response.data[0].embedding
