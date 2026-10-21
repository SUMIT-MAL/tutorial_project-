"""
This module defines the configuration settings for the application using Pydantic's BaseSettings class. It reads environment variables from a .env file and provides a structured way to access configuration values.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    """
    This class defines the configuration settings for the application.
    """
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8")

    MODEL_NAME: str

    TRAVILY_API: str

    LANGSMITH_TRACING: str
    LANGSMITH_ENDPOINT: str
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str

    GROQ_API_KEY: str
    SERPAPI_API: str


seetings_manager = ApiSettings()
