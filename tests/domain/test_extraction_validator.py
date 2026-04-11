from app.domain.extraction_validator import ExtractionValidator


def test_validate_and_normalize_smoke():
    validator = ExtractionValidator()

    llm_output = {
        "task_type": "PREDICTION",
        "process_type": "ETCH",
        "process_params": {
            "pressure": {
                "value": 20,
                "unit": "mTorr",
            },
            "source_power": {
                "value": 600,
                "unit": "W",
            },
            "bias_power": {
                "value": 100,
                "unit": "W",
            },
        }
    }

    response = validator.validate_and_normalize(
        request_id="req-001",
        llm_output=llm_output,
    )

    # Pydantic v2 / v1 모두 대응
    dumped = response.model_dump() if hasattr(response, "model_dump") else response.dict()

    assert dumped["request_id"] == "req-001"