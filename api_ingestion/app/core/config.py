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
    return f"postgresql+psycopg2://{get_database_user()}:{get_database_password()}@{get_database_host()}:{get_database_port()}/{get_database_name()}"


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


def get_database_host():
    """Retrieve the database host from environment variables."""
    return os.getenv("DATABASE_HOST", "localhost")


def get_database_port():
    """Retrieve the database port from environment variables."""
    return os.getenv("DATABASE_PORT", "5432")


def get_database_user():
    """Retrieve the database user from environment variables."""
    return os.getenv("DATABASE_USER", "testuser")


def get_database_password():
    """Retrieve the database password from environment variables."""
    return os.getenv("DATABASE_PASSWORD", "testpwd")


def get_database_name():
    """Retrieve the database name from environment variables."""
    return os.getenv("DATABASE_NAME", "vectordb")
