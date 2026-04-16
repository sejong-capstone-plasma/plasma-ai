import pytest

from app.domain.input_preprocessor import InputPreprocessor


def test_clean_success():
    preprocessor = InputPreprocessor(max_length=100)

    result = preprocessor.clean("   pressure 20 mTorr   ")

    assert result == "pressure 20 mTorr"


def test_clean_collapses_whitespace():
    preprocessor = InputPreprocessor(max_length=100)

    result = preprocessor.clean("pressure   20\n\nmTorr\t source power 600W")

    assert result == "pressure 20 mTorr source power 600W"


def test_clean_raises_when_none():
    preprocessor = InputPreprocessor()

    with pytest.raises(ValueError, match="user_input이 없습니다"):
        preprocessor.clean(None)


def test_clean_raises_when_blank():
    preprocessor = InputPreprocessor()

    with pytest.raises(ValueError, match="user_input이 비어 있습니다"):
        preprocessor.clean("    ")


def test_clean_raises_when_too_long():
    preprocessor = InputPreprocessor(max_length=5)

    with pytest.raises(ValueError, match="초과"):
        preprocessor.clean("123456")