from __future__ import annotations

import re
import unicodedata

from app.core.exceptions import ValidationException

class InputPreprocessor:
    def __init__(self, max_length: int = 500) -> None:
        self.max_length = max_length

    def clean(self, user_input: str) -> str:
        if user_input is None:
            raise ValidationException(
                message="user_input이 없습니다.",
                details={"field": "user_input", "reason": "missing"},
            )

        text = unicodedata.normalize("NFKC", user_input)
        text = text.strip()

        if not text:
            raise ValidationException(
                message="user_input이 비어 있습니다.",
                details={"field": "user_input", "reason": "empty"},
            )

        text = text.replace("\x00", " ")
        text = re.sub(r"\s+", " ", text).strip()

        if len(text) > self.max_length:
            raise ValidationException(
                message=f"user_input 길이가 {self.max_length}자를 초과했습니다.",
                details={
                    "field": "user_input",
                    "reason": "too_long",
                    "max_length": self.max_length,
                },
            )

        return text