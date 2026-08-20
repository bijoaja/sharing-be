from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_ENV: str = "development"
    DEBUG: bool = True
    ARTICLE_PORT: int = 8001
    DATABASE_URL: str
    # Root credential — used only by alembic (env.py) to bootstrap the
    # database and grant privileges to the app user in DATABASE_URL above.
    # Not used by the running app itself.
    MYSQL_ROOT_PASSWORD: str = ""

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local", ".env.production"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
