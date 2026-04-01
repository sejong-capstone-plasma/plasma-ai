from fastapi import APIRouter

from app.core.config import settings
from app.llm.client import LLMClient

router = APIRouter()


@router.get("/")
async def health_check():
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "app_env": settings.app_env,
        "llm_provider": settings.llm_provider,
        "llm_model": settings.llm_model,
        "llm_base_url": settings.llm_base_url,
    }


@router.get("/llm")
async def health_check_llm():
    client = LLMClient()

    try:
        content = await client.chat(
            system_prompt="You are a health check assistant.",
            user_prompt="Say OK.",
        )

        return {
            "status": "ok",
            "service": "ai-app",
            "llm_status": "connected",
            "model": client.model,
            "response": content,
        }

    except Exception as e:
        return {
            "status": "error",
            "service": "ai-app",
            "llm_status": "disconnected",
            "model": client.model,
            "error": str(e),
        }