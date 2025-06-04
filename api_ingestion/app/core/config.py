# Environment/config loading
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_openai_api_key():
    """Retrieve the OpenAI API key from environment variables."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return api_key


def get_database_url():
    """Retrieve the database URL from environment variables."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    return db_url


def get_openai_model_embedding():
    """Retrieve the OpenAI model for embedding from environment variables."""
    model = os.getenv("OPENAI_MODEL_EMBEDDING", "text-embedding-3-small")
    return model


def get_openai_mock_enable():
    """Check if OpenAI mocking is enabled."""
    return os.getenv("OPENAI_MOCK_ENABLE", "true").lower() == "true"


def get_database_mock_enable():
    """Check if database mocking is enabled."""
    return os.getenv("DATABASE_MOCK_ENABLE", "true").lower() == "true"
