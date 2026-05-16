import pytest

from app.core.enums import ProcessType, TaskType, ValidationStatus
from app.domain.handlers.question_handler import QuestionHandler
from app.schemas.extract import ExtractParametersRequest


class _DummyLLMClient:
    async def chat_with_history_from_file(self, **kwargs): ...
    def extract_json(self, text): ...


class _DummyParser:
    def parse(self, raw): ...


class _DummyValidator:
    def validate_and_normalize(self, **kwargs): ...


@pytest.fixture
def handler():
    return QuestionHandler(
        llm_client=_DummyLLMClient(),
        llm_extraction_parser=_DummyParser(),
        extraction_validator=_DummyValidator(),
    )


@pytest.fixture
def request_obj():
    return ExtractParametersRequest(
        request_id="req-q-001",
        user_input="ion flux가 뭐야?",
    )


@pytest.mark.asyncio
async def test_question_handler_returns_valid(handler, request_obj):
    response = await handler.execute(
        request=request_obj,
        cleaned_input="ion flux가 뭐야?",
        history=[],
        task_type=TaskType.QUESTION,
        process_type=ProcessType.ETCH,
    )

    assert response.request_id == "req-q-001"
    assert response.validation_status == ValidationStatus.VALID
    assert response.task_type == TaskType.QUESTION
    assert response.process_type == ProcessType.ETCH


@pytest.mark.asyncio
async def test_question_handler_has_no_params(handler, request_obj):
    response = await handler.execute(
        request=request_obj,
        cleaned_input="ion flux가 뭐야?",
        history=[],
        task_type=TaskType.QUESTION,
        process_type=ProcessType.ETCH,
    )

    assert response.process_params is None
    assert response.current_outputs is None
    assert response.condition_a is None
    assert response.condition_b is None


@pytest.mark.asyncio
async def test_question_handler_does_not_call_llm(request_obj):
    class TrackingLLMClient:
        def __init__(self):
            self.called = False

        async def chat_with_history_from_file(self, **kwargs):
            self.called = True

        def extract_json(self, text): ...

    tracking_llm = TrackingLLMClient()
    handler = QuestionHandler(
        llm_client=tracking_llm,
        llm_extraction_parser=_DummyParser(),
        extraction_validator=_DummyValidator(),
    )

    await handler.execute(
        request=request_obj,
        cleaned_input="ion flux가 뭐야?",
        history=[],
        task_type=TaskType.QUESTION,
        process_type=ProcessType.ETCH,
    )

    assert not tracking_llm.called
