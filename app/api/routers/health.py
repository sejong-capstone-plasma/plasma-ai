from fastapi import APIRouter
from app.llm.client import get_llm_client, get_llm_model_name

from app.core.config import settings

router = APIRouter()


@router.get("")
def health_check():
    return {
        "status": "ok",
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION,
        "app_env": settings.APP_ENV,
        "llm_provider": settings.LLM_PROVIDER,
        "llm_model": settings.LLM_MODEL,
        "llm_base_url": settings.LLM_BASE_URL,
    }


@router.get("/llm")
def health_check_llm():
    client = get_llm_client()
    model_name = get_llm_model_name()

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a health check assistant."},
                {"role": "user", "content": "Say OK."},
            ],
            temperature=0.0,
            max_tokens=10,
        )

        content = response.choices[0].message.content

        return {
            "status": "ok",
            "service": "ai-app",
            "llm_status": "connected",
            "model": model_name,
            "response": content,
        }

    except Exception as e:
        return {
            "status": "error",
            "service": "ai-app",
            "llm_status": "disconnected",
            "model": model_name,
            "error": str(e),
        }