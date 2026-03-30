from app.schemas.explanation import ExplanationRequest, ExplanationResponse


class ExplanationService:
    def execute(self, request: ExplanationRequest) -> ExplanationResponse:
        if request.task_type == "PREDICTION":
            return ExplanationResponse(
                request_id=request.request_id,
                summary="입력 조건 기준으로 이온 밀도는 높고 이온 온도는 중간 수준으로 예측됩니다.",
                details=[
                    "source power가 상대적으로 높아 이온 밀도 증가에 영향을 준 것으로 해석됩니다."
                ],
            )

        return ExplanationResponse(
            request_id=request.request_id,
            summary="목표 조건에 가장 근접한 후보 공정 조건을 도출했습니다.",
            details=[
                "압력을 소폭 낮추고 source power를 높이며 bias power를 다소 낮춘 조건이 목표값에 가장 근접했습니다.",
                "상위 후보들 간 점수 차이가 크지 않아 추가 제약조건이 있으면 재탐색이 가능합니다.",
            ],
        )