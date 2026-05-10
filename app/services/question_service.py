from __future__ import annotations

from app.schemas.pipelines import QuestionPipelineRequest, QuestionPipelineResponse


class QuestionService:
    async def execute(self, request: QuestionPipelineRequest) -> QuestionPipelineResponse:
        raise NotImplementedError
