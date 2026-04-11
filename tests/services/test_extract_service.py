import json
import pytest

from app.schemas.extract import ExtractParametersRequest
from app.services.extract_service import ExtractService


class FakeInputPreprocessor:
    def __init__(self):
        self.called_with = None

    def clean(self, user_input: str) -> str:
        self.called_with = user_input
        return user_input.strip()


class FakeLLMClient:
    def __init__(self):
        self.called_with = None

    async def chat_from_file(self, prompt_file: str, user_prompt: str) -> str:
        self.called_with = {
            "prompt_file": prompt_file,
            "user_prompt": user_prompt,
        }
        return """
        ```json
        {
          "task_type": "PREDICTION",
          "process_type": "ETCH",
          "process_params": {
            "pressure": {"value": 20, "unit": "mTorr"},
            "source_power": {"value": 600, "unit": "W"},
            "bias_power": {"value": 100, "unit": "W"}
          }
        }
        ```
        """

    def extract_json(self, raw_text: str) -> dict:
        # 실제 extract_json 대신 단순화
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1
        return json.loads(raw_text[start:end])


class FakeExtractionValidator:
    def __init__(self, result):
        self.called_with = None
        self.result = result

    def validate_and_normalize(self, request_id: str, llm_output: dict):
        self.called_with = {
            "request_id": request_id,
            "llm_output": llm_output,
        }
        return self.result


@pytest.mark.asyncio
async def test_execute_success_flow():
    fake_preprocessor = FakeInputPreprocessor()
    fake_llm = FakeLLMClient()
    fake_result = {"status": "ok"}  # 실제 응답 모델 대신 sentinel
    fake_validator = FakeExtractionValidator(result=fake_result)

    service = ExtractService(
        llm_client=fake_llm,
        input_preprocessor=fake_preprocessor,
        extraction_validator=fake_validator,
        prompt_file="app/llm/prompts/extract_system.txt",
    )

    request = ExtractParametersRequest(
        request_id="req-001",
        user_input="  pressure 20 mTorr, source power 600 W, bias power 100 W  ",
    )

    response = await service.execute(request)

    # 1) 전처리 호출 확인
    assert fake_preprocessor.called_with == "  pressure 20 mTorr, source power 600 W, bias power 100 W  "

    # 2) LLM user prompt 생성 확인
    sent_prompt = json.loads(fake_llm.called_with["user_prompt"])
    assert sent_prompt["request_id"] == "req-001"
    assert sent_prompt["user_input"] == "pressure 20 mTorr, source power 600 W, bias power 100 W"

    # 3) validator 호출 확인
    assert fake_validator.called_with["request_id"] == "req-001"
    assert fake_validator.called_with["llm_output"]["task_type"] == "PREDICTION"
    assert fake_validator.called_with["llm_output"]["process_type"] == "ETCH"

    # 4) 최종 반환 확인
    assert response == fake_result


@pytest.mark.asyncio
async def test_execute_raises_when_llm_json_parse_fails():
    class BrokenLLMClient(FakeLLMClient):
        async def chat_from_file(self, prompt_file: str, user_prompt: str) -> str:
            return "not a json response"

        def extract_json(self, raw_text: str) -> dict:
            raise ValueError("no json found")

    service = ExtractService(
        llm_client=BrokenLLMClient(),
        input_preprocessor=FakeInputPreprocessor(),
        extraction_validator=FakeExtractionValidator(result={"status": "ok"}),
        prompt_file="app/llm/prompts/extract_system.txt",
    )

    request = ExtractParametersRequest(
        request_id="req-002",
        user_input="pressure 20",
    )

    with pytest.raises(ValueError, match="LLM 응답 JSON 파싱 실패"):
        await service.execute(request)