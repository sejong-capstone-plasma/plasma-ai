import os
from openai import OpenAI


def get_llm_client() -> OpenAI:
    return OpenAI(
        base_url=os.getenv("LLM_BASE_URL", "http://ai-vllm:8000/v1"),
        api_key=os.getenv("LLM_API_KEY", "local-ai-token"),
    )


def get_llm_model_name() -> str:
    return os.getenv("LLM_MODEL_NAME", "/models/Qwen2.5-1.5B-Instruct")