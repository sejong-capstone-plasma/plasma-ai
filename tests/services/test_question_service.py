import json

import pytest

from app.rag.base_retriever import BaseRetriever
from app.schemas.question import (
    QuestionPipelineRequest,
    SourceDocument,
    SourceMetadata,
)
from app.services.question_service import QuestionService


class FakeLLMClient:
    def __init__(self, answer: str = "ion flux는 단위 면적·시간당 이온 수입니다."):
        self.answer = answer
        self.called_history = None
        self.called_user_prompt = None

    async def chat_with_history_from_file(
        self, prompt_file: str, history: list, user_prompt: str
    ) -> str:
        self.called_history = history
        self.called_user_prompt = user_prompt
        return json.dumps({"request_id": "req-001", "answer": self.answer})

    @staticmethod
    def extract_json(raw_text: str) -> dict:
        return json.loads(raw_text)


class FakeRetriever(BaseRetriever):
    def __init__(self, docs: list[SourceDocument] | None = None):
        self.docs = docs or []

    async def retrieve(self, query: str) -> list[SourceDocument]:
        return self.docs


@pytest.fixture
def request_obj():
    return QuestionPipelineRequest(
        request_id="req-001",
        original_user_input="ion flux가 뭐야?",
        history=[],
    )


@pytest.mark.asyncio
async def test_returns_answer(request_obj):
    service = QuestionService(llm_client=FakeLLMClient(), retriever=FakeRetriever())
    response = await service.execute(request_obj)

    assert response.request_id == "req-001"
    assert response.answer == "ion flux는 단위 면적·시간당 이온 수입니다."
    assert response.sources == []


@pytest.mark.asyncio
async def test_sources_from_retriever(request_obj):
    doc = SourceDocument(
        title="플랫폼 개요",
        chunk="ion flux는 cm⁻²s⁻¹ 단위입니다.",
        score=0.9,
        metadata=SourceMetadata(source="data/knowledge/raw/platform_overview.md"),
    )
    service = QuestionService(llm_client=FakeLLMClient(), retriever=FakeRetriever(docs=[doc]))
    response = await service.execute(request_obj)

    assert len(response.sources) == 1
    assert response.sources[0].title == "플랫폼 개요"


@pytest.mark.asyncio
async def test_context_included_in_user_prompt(request_obj):
    doc = SourceDocument(
        title="플랫폼 개요",
        chunk="ion flux 설명 텍스트",
        score=0.85,
        metadata=SourceMetadata(source="data/knowledge/raw/platform_overview.md"),
    )
    llm = FakeLLMClient()
    service = QuestionService(llm_client=llm, retriever=FakeRetriever(docs=[doc]))
    await service.execute(request_obj)

    payload = json.loads(llm.called_user_prompt)
    assert "ion flux 설명 텍스트" in payload["context"]


@pytest.mark.asyncio
async def test_history_passed_to_llm(request_obj):
    from app.schemas.extract import ChatMessage

    request_with_history = QuestionPipelineRequest(
        request_id="req-001",
        original_user_input="더 자세히 설명해줘",
        history=[ChatMessage(role="user", content="ion flux가 뭐야?")],
    )
    llm = FakeLLMClient()
    service = QuestionService(llm_client=llm, retriever=FakeRetriever())
    await service.execute(request_with_history)

    assert llm.called_history == [{"role": "user", "content": "ion flux가 뭐야?"}]
