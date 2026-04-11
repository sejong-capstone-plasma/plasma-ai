from __future__ import annotations

import re
import unicodedata


class InputPreprocessor:
    def __init__(self, max_length: int = 500) -> None:
        self.max_length = max_length

    def clean(self, user_input: str) -> str:
        if user_input is None:
            raise ValueError("user_input이 없습니다.")

        text = unicodedata.normalize("NFKC", user_input)
        text = text.strip()

        if not text:
            raise ValueError("user_input이 비어 있습니다.")

        # 제어문자 정리
        text = text.replace("\x00", " ")
        text = re.sub(r"\s+", " ", text).strip()

        if len(text) > self.max_length:
            raise ValueError(f"user_input 길이가 {self.max_length}자를 초과했습니다.")

        return text