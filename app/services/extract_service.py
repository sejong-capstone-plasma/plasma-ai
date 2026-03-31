from app.core.enums import GoalType, ProcessType, TaskType, ValidationStatus
from app.llm.client import LLMClient
from app.schemas.common import GoalSpec, ValueWithUnit
from app.schemas.extract import ExtractParametersRequest, ExtractParametersResponse


class ExtractService:
    def __init__(self) -> None:
        self.llm_client = LLMClient()
        self.prompt_file = "app/llm/prompts/extract_parameters.json"

    async def extract_parameters(self, text: str) -> tuple[str, dict]:
        raw_text = await self.llm_client.chat_from_file(
            prompt_file=self.prompt_file,
            user_prompt=text,
        )
        parsed = self.llm_client.extract_json(raw_text)
        return raw_text, parsed

    def execute(self, request: ExtractParametersRequest) -> ExtractParametersResponse:
        _normalized_text = request.user_input.strip()

        return ExtractParametersResponse(
            request_id=request.request_id,
            task_type=TaskType.OPTIMIZATION,
            process_type=ProcessType.ETCH,
            process_params={
                "pressure_mtorr": ValueWithUnit(value=20, unit="mTorr"),
                "source_power_w": ValueWithUnit(value=500, unit="W"),
                "bias_power_w": ValueWithUnit(value=200, unit="W"),
            },
            target_specs={
                "ion_density_cm3": GoalSpec(
                    goal_type=GoalType.EXACT,
                    target_value=1.0e11,
                    unit="cm3",
                ),
                "ion_temp_ev": GoalSpec(
                    goal_type=GoalType.EXACT,
                    target_value=4.0,
                    unit="eV",
                ),
            },
            validation_status=ValidationStatus.COMPLETE,
            missing_fields=[],
        )