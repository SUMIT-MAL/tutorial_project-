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

    APIFY_CLIENT_API: str
    Actor_id: str


seetings_manager = ApiSettings()
