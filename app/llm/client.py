import json
import re
from pathlib import Path
from typing import Any

from openai import AsyncOpenAI

from app.core.config import settings


class LLMClient:
    def __init__(self) -> None:
        self.client = AsyncOpenAI(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
            timeout=settings.llm_timeout,
        )
        self.model = settings.llm_model
        self.temperature = settings.llm_temperature
        self.max_tokens = settings.llm_max_tokens

    async def chat(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
        except Exception as e:
            raise RuntimeError(f"LLM 호출 실패: {e}") from e

        if not response.choices:
            raise ValueError("LLM 응답에 choices가 없습니다.")

        content = response.choices[0].message.content
        if not content:
            raise ValueError("LLM 응답 content가 비어 있습니다.")

        return content

    async def chat_from_file(self, prompt_file: str, user_prompt: str) -> str:
        prompt_path = Path(prompt_file).resolve()
        system_prompt = prompt_path.read_text(encoding="utf-8")
        return await self.chat(system_prompt=system_prompt, user_prompt=user_prompt)

    @staticmethod
    def extract_json(text: str) -> dict[str, Any]:
        text = text.strip()

        # 1. 응답 전체가 JSON인 경우
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # 2. fenced code block 안 JSON 추출
        fenced_match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
        if fenced_match:
            block = fenced_match.group(1).strip()
            try:
                return json.loads(block)
            except json.JSONDecodeError:
                text = block

        # 3. balanced brace 방식으로 첫 JSON 객체 추출
        start = text.find("{")
        while start != -1:
            depth = 0
            for i in range(start, len(text)):
                if text[i] == "{":
                    depth += 1
                elif text[i] == "}":
                    depth -= 1
                    if depth == 0:
                        candidate = text[start:i + 1]
                        try:
                            return json.loads(candidate)
                        except json.JSONDecodeError:
                            break
            start = text.find("{", start + 1)

        raise ValueError("LLM 응답에서 JSON 객체를 찾을 수 없습니다.")