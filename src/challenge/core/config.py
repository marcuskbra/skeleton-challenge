"""
Application configuration management.

Add configuration settings here when needed, such as:
- Environment variables
- Database connection strings
- API keys and secrets
- Feature flags

Example using Pydantic Settings:
    from pydantic_settings import BaseSettings

    class Settings(BaseSettings):
        database_url: str
        api_key: str

        class Config:
            env_file = ".env"
"""
