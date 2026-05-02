import json
import re
from pathlib import Path
from typing import Any

from openai import AsyncOpenAI

from app.core.config import settings
from app.core.exceptions import ModelInferenceException, ModelNotReadyException

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
        extra: dict = {}
        if settings.llm_provider == "vllm":
            extra["extra_body"] = {"chat_template_kwargs": {"enable_thinking": False}}

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                **extra,
            )
        except Exception as e:
            raise ModelInferenceException(
                message="LLM 호출에 실패했습니다.",
                details={"reason": str(e)},
            ) from e

        if not response.choices:
            raise ModelInferenceException(
                message="LLM 응답에 choices가 없습니다.",
                details={},
            )

        content = response.choices[0].message.content
        if not content:
            raise ModelInferenceException(
                message="LLM 응답 content가 비어 있습니다.",
                details={},
            )

        return content

    async def chat_with_history(
        self,
        system_prompt: str,
        history: list[dict[str, str]],
        user_prompt: str,
    ) -> str:
        extra: dict = {}
        if settings.llm_provider == "vllm":
            extra["extra_body"] = {"chat_template_kwargs": {"enable_thinking": False}}

        messages: list[dict] = [{"role": "system", "content": system_prompt}]
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_prompt})

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                messages=messages,
                **extra,
            )
        except Exception as e:
            raise ModelInferenceException(
                message="LLM 호출에 실패했습니다.",
                details={"reason": str(e)},
            ) from e

        if not response.choices:
            raise ModelInferenceException(
                message="LLM 응답에 choices가 없습니다.",
                details={},
            )

        content = response.choices[0].message.content
        if not content:
            raise ModelInferenceException(
                message="LLM 응답 content가 비어 있습니다.",
                details={},
            )

        return content

    async def chat_with_history_from_file(
        self,
        prompt_file: str,
        history: list[dict[str, str]],
        user_prompt: str,
    ) -> str:
        try:
            prompt_path = Path(prompt_file).resolve()
            system_prompt = prompt_path.read_text(encoding="utf-8")
        except FileNotFoundError as e:
            raise ModelNotReadyException(
                message="프롬프트 파일을 찾을 수 없습니다.",
                details={"prompt_file": prompt_file},
            ) from e
        except Exception as e:
            raise ModelNotReadyException(
                message="프롬프트 파일을 읽는 데 실패했습니다.",
                details={"prompt_file": prompt_file, "reason": str(e)},
            ) from e

        return await self.chat_with_history(
            system_prompt=system_prompt,
            history=history,
            user_prompt=user_prompt,
        )

    async def chat_from_file(self, prompt_file: str, user_prompt: str) -> str:
        try:
            prompt_path = Path(prompt_file).resolve()
            system_prompt = prompt_path.read_text(encoding="utf-8")
        except FileNotFoundError as e:
            raise ModelNotReadyException(
                message="프롬프트 파일을 찾을 수 없습니다.",
                details={"prompt_file": prompt_file},
            ) from e
        except Exception as e:
            raise ModelNotReadyException(
                message="프롬프트 파일을 읽는 데 실패했습니다.",
                details={"prompt_file": prompt_file, "reason": str(e)},
            ) from e

        return await self.chat(system_prompt=system_prompt, user_prompt=user_prompt)

    @staticmethod
    def extract_json(text: str) -> dict[str, Any]:
        text = text.strip()
        
        # Qwen3 등 thinking model의 <think>...</think> 블록 제거
        text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

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

        raise ModelInferenceException(
            message="LLM 응답에서 JSON 객체를 찾을 수 없습니다.",
            details={"raw_text_preview": text[:300]},
        )