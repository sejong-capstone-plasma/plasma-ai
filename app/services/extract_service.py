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

    async def execute(
        self,
        request: ExtractParametersRequest,
    ) -> ExtractParametersResponse:
        cleaned_input = self._input_preprocessor.clean(request.user_input)
        history = [{"role": msg.role, "content": msg.content} for msg in request.history]

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
