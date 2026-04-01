import os
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]

CURRENT_APP_ENV = os.getenv("APP_ENV", "local").lower()

ENV_FILE_MAP = {
    "local": BASE_DIR / ".env.local",
    "prod": BASE_DIR / ".env.prod",
}

SELECTED_ENV_FILE = ENV_FILE_MAP.get(CURRENT_APP_ENV, BASE_DIR / ".env.local")

DEFAULT_LLM_BASE_URL = (
    "http://ai-vllm:8000/v1"
    if CURRENT_APP_ENV == "prod"
    else "http://host.docker.internal:11434/v1"
)


class Settings(BaseSettings):
    app_name: str = Field(default="plasma-ai", alias="APP_NAME")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    app_description: str = Field(
        default="Backend ↔ AI internal API server",
        alias="APP_DESCRIPTION",
    )

    app_env: Literal["local", "prod"] = Field(default=CURRENT_APP_ENV, alias="APP_ENV")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")

    debug: bool = Field(default=True, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    model_dir: Path = Field(default=BASE_DIR / "data" / "models", alias="MODEL_DIR")
    hf_cache_dir: Path = Field(default=BASE_DIR / "data" / "hf_cache", alias="HF_CACHE_DIR")
    output_dir: Path = Field(default=BASE_DIR / "data" / "outputs", alias="OUTPUT_DIR")

    llm_provider: Literal["ollama", "vllm"] = Field(default="ollama", alias="LLM_PROVIDER")
    llm_base_url: str = Field(default=DEFAULT_LLM_BASE_URL, alias="LLM_BASE_URL")
    llm_api_key: str = Field(default="ollama", alias="LLM_API_KEY")
    llm_model: str = Field(default="qwen2.5:7b", alias="LLM_MODEL")
    llm_model_path: str = Field(default="qwen2.5:7b", alias="LLM_MODEL_PATH")
    llm_timeout: float = Field(default=120.0, alias="LLM_TIMEOUT")
    llm_temperature: float = Field(default=0.1, alias="LLM_TEMPERATURE")
    llm_max_tokens: int = Field(default=1024, alias="LLM_MAX_TOKENS")

    hf_hub_offline: bool = Field(default=False, alias="HF_HUB_OFFLINE")
    transformers_offline: bool = Field(default=False, alias="TRANSFORMERS_OFFLINE")

    @field_validator("model_dir", "hf_cache_dir", "output_dir", mode="before")
    @classmethod
    def resolve_relative_path(cls, v):
        path = Path(v)
        if not path.is_absolute():
            return BASE_DIR / path
        return path

    model_config = SettingsConfigDict(
        env_file=SELECTED_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


settings = Settings()