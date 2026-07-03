from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    database_url: str
    secret_key: str
    environment: str = "development"
    debug: bool = True
    cors_origins: list[str] = ["http://localhost:5173"]

settings = Settings()