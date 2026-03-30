from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Semiconductor Process AI Server"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "Backend ↔ AI internal API server"

    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    MODEL_DIR: str = "data/models"
    HF_CACHE_DIR: str = "data/hf_cache"
    OUTPUT_DIR: str = "data/outputs"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()