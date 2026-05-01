from __future__ import annotations

from typing import Any

from app.core.enums import ProcessType, TaskType
from app.core.exceptions import ModelInferenceException


class LLMClassificationParser:
    def parse(self, llm_output: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(llm_output, dict):
            raise ModelInferenceException(
                message="LLM 분류 출력 형식이 올바르지 않습니다.",
                details={
                    "reason": "llm_output_must_be_object",
                    "actual_type": type(llm_output).__name__,
                },
            )

        return {
            "task_type": self._parse_task_type(llm_output.get("task_type")),
            "process_type": self._parse_process_type(llm_output.get("process_type")),
        }

    def _parse_task_type(self, raw: Any) -> TaskType:
        try:
            return TaskType(raw)
        except Exception:
            return TaskType.UNSUPPORTED

    def _parse_process_type(self, raw: Any) -> ProcessType:
        try:
            return ProcessType(raw)
        except Exception:
            return ProcessType.UNKNOWN
