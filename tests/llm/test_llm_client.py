import pytest

from app.llm.client import LLMClient


class DummyLLMClient(LLMClient):
    def __init__(self):
        # 부모 __init__ 생략
        self.called = {}

    async def chat(self, system_prompt: str, user_prompt: str) -> str:
        self.called["system_prompt"] = system_prompt
        self.called["user_prompt"] = user_prompt
        return '{"ok": true}'


def test_extract_json_success():
    # __init__ 안 타고 인스턴스만 생성
    client = object.__new__(LLMClient)

    raw_text = """
    아래는 결과입니다.
    ```json
    {
      "task_type": "PREDICTION",
      "process_type": "ETCH"
    }
    ```
    """

    parsed = client.extract_json(raw_text)

    assert parsed["task_type"] == "PREDICTION"
    assert parsed["process_type"] == "ETCH"


def test_extract_json_raises_on_invalid_text():
    client = object.__new__(LLMClient)

    with pytest.raises(Exception):
        client.extract_json("this is not json")


@pytest.mark.asyncio
async def test_chat_from_file_reads_prompt_and_calls_chat(tmp_path):
    prompt_file = tmp_path / "extract_system.txt"
    prompt_file.write_text("SYSTEM PROMPT TEST", encoding="utf-8")

    client = DummyLLMClient()

    result = await client.chat_from_file(
        prompt_file=str(prompt_file),
        user_prompt='{"request_id":"req-001","user_input":"test"}',
    )

    assert result == '{"ok": true}'
    assert client.called["system_prompt"] == "SYSTEM PROMPT TEST"
    assert client.called["user_prompt"] == '{"request_id":"req-001","user_input":"test"}'