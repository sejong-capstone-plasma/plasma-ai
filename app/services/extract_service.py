from __future__ import annotations

import json
from pathlib import Path

from app.core.enums import TaskType
from app.domain.extraction_validator import ExtractionValidator
from app.domain.handlers.base import BaseTaskHandler
from app.domain.handlers.comparison_handler import ComparisonHandler
from app.domain.handlers.optimization_handler import OptimizationHandler
from app.domain.handlers.prediction_handler import PredictionHandler
from app.domain.handlers.question_handler import QuestionHandler
from app.domain.handlers.unsupported_handler import UnsupportedHandler
from app.domain.input_preprocessor import InputPreprocessor
from app.domain.llm_classification_parser import LLMClassificationParser
from app.domain.llm_extraction_parser import LLMExtractionParser
from app.llm.client import LLMClient
from app.schemas.extract import ExtractParametersRequest, ExtractParametersResponse

_PROMPTS_DIR = Path(__file__).resolve().parents[1] / "llm" / "prompts"


class ExtractService:
    def __init__(
        self,
        llm_client: LLMClient | None = None,
        input_preprocessor: InputPreprocessor | None = None,
        llm_classification_parser: LLMClassificationParser | None = None,
        llm_extraction_parser: LLMExtractionParser | None = None,
        extraction_validator: ExtractionValidator | None = None,
        classify_prompt_file: str | None = None,
    ) -> None:
        self._llm_client = llm_client or LLMClient()
        self._input_preprocessor = input_preprocessor or InputPreprocessor()
        self._llm_classification_parser = llm_classification_parser or LLMClassificationParser()
        self._classify_prompt_file = classify_prompt_file or str(
            _PROMPTS_DIR / "classify_system.txt"
        )

        handler_kwargs = dict(
            llm_client=self._llm_client,
            llm_extraction_parser=llm_extraction_parser or LLMExtractionParser(),
            extraction_validator=extraction_validator or ExtractionValidator(),
        )
        self._handlers: dict[TaskType, BaseTaskHandler] = {
            TaskType.PREDICTION: PredictionHandler(**handler_kwargs),
            TaskType.OPTIMIZATION: OptimizationHandler(**handler_kwargs),
            TaskType.COMPARISON: ComparisonHandler(**handler_kwargs),
            TaskType.QUESTION: QuestionHandler(**handler_kwargs),
            TaskType.UNSUPPORTED: UnsupportedHandler(**handler_kwargs),
        }

    @staticmethod
    def _format_params(params: dict) -> str:
        order = ["pressure", "source_power", "bias_power"]
        parts = []
        for key in order:
            if key in params:
                v = params[key]
                parts.append(f"{key} {v.get('value')} {v.get('unit', '')}")
        return ", ".join(parts)

    @staticmethod
    def _simplify_assistant_message(content: str) -> str:
        try:
            data = json.loads(content)
        except (json.JSONDecodeError, TypeError):
            return content

        details = data.get("details", {})
        if not details:
            return data.get("summary", content)

        lines = []
        summary = data.get("summary", "")
        if summary:
            lines.append(summary)

        # prediction
        if "prediction_result" in details and "process_params" in details:
            params = ExtractService._format_params(details["process_params"])
            pr = details["prediction_result"]
            score = pr.get("etch_score", {}).get("value", "?")
            lines.append(f"예측 조건: {params} → etch_score {score}")

        # optimization
        if "optimization_result" in details and "process_params" in details:
            orig = ExtractService._format_params(details["process_params"])
            orig_score = details.get("baseline_outputs", {}).get("etch_score", {}).get("value", "?")
            lines.append(f"원래 조건: {orig}, etch_score {orig_score}")
            candidates = details["optimization_result"].get("optimization_candidates", [])
            for c in candidates:
                rank = c.get("rank")
                params = ExtractService._format_params(c.get("process_params", {}))
                score = c.get("prediction_result", {}).get("etch_score", {}).get("value", "?")
                lines.append(f"개선 조건 {rank}순위: {params}, etch_score {score}")

        # comparison
        if "condition_a" in details and "condition_b" in details:
            interpretation = details.get("interpretation", {})
            winner = interpretation.get("winning_condition")
            label_map = {"condition_a": "조건 A (조건 1)", "condition_b": "조건 B (조건 2)"}
            for key, label in [("condition_a", "조건 A (조건 1)"), ("condition_b", "조건 B (조건 2)")]:
                cond = details[key]
                params = ExtractService._format_params(cond.get("process_params", {}))
                score = cond.get("prediction_result", {}).get("etch_score", {}).get("value", "?")
                win_marker = " ← 이긴 조건" if winner == key else ""
                lines.append(f"{label}: {params}, etch_score {score}{win_marker}")

        return "\n".join(lines) if lines else content

    def _simplify_history(self, history: list[dict]) -> list[dict]:
        result = []
        for msg in history:
            if msg["role"] == "assistant":
                result.append({"role": "assistant", "content": self._simplify_assistant_message(msg["content"])})
            else:
                result.append(msg)
        return result

    async def execute(
        self,
        request: ExtractParametersRequest,
    ) -> ExtractParametersResponse:
        cleaned_input = self._input_preprocessor.clean(request.user_input)
        history = self._simplify_history(
            [{"role": msg.role, "content": msg.content} for msg in request.history]
        )

        # Step 1: Classify task_type + process_type (with history context)
        classify_user_prompt = json.dumps(
            {"user_input": cleaned_input},
            ensure_ascii=False,
        )
        classify_raw = await self._llm_client.chat_with_history_from_file(
            prompt_file=self._classify_prompt_file,
            history=history,
            user_prompt=classify_user_prompt,
        )
        classify_output = self._llm_client.extract_json(classify_raw)
        classify_parsed = self._llm_classification_parser.parse(classify_output)

        task_type = classify_parsed["task_type"]
        process_type = classify_parsed["process_type"]

        # Step 2: Dispatch to task-specific handler
        handler = self._handlers[task_type]
        return await handler.execute(
            request=request,
            cleaned_input=cleaned_input,
            history=history,
            task_type=task_type,
            process_type=process_type,
        )
