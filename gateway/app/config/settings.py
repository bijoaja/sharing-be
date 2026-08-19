from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_ENV: str = "development"
    DEBUG: bool = True
    GATEWAY_PORT: int = 8000
    ARTICLE_SERVICE_URL: str

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local", ".env.production"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
