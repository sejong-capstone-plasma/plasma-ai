import pytest

from app.rag.chunker import Chunker


def test_empty_returns_empty():
    assert Chunker().chunk("") == []


def test_whitespace_returns_empty():
    assert Chunker().chunk("   \n\n  ") == []


def test_short_text_single_chunk():
    text = "ion flux는 단위 면적·시간당 이온 수입니다."
    chunks = Chunker(chunk_size=500).chunk(text)
    assert chunks == [text]


def test_long_text_is_split():
    text = ("A" * 300 + "\n\n") * 5
    chunks = Chunker(chunk_size=500, overlap=50).chunk(text)
    assert len(chunks) > 1


def test_no_chunk_exceeds_chunk_size():
    text = ("단락 텍스트입니다. " * 20 + "\n\n") * 10
    chunker = Chunker(chunk_size=200, overlap=40)
    for chunk in chunker.chunk(text):
        assert len(chunk) <= 200


def test_overlap_content_carried_over():
    # 두 번째 청크는 첫 번째 청크 끝부분 텍스트를 포함해야 한다
    para1 = "첫 번째 단락입니다." * 30   # ~300 chars
    para2 = "두 번째 단락입니다." * 30
    text = para1 + "\n\n" + para2
    chunker = Chunker(chunk_size=300, overlap=80)
    chunks = chunker.chunk(text)
    assert len(chunks) >= 2
    # 두 번째 청크는 첫 번째 청크의 끝부분을 포함해야 한다
    assert chunks[0][-50:] in chunks[1] or chunks[1].startswith(chunks[0][-30:])


def test_paragraph_boundary_respected():
    para1 = "첫 단락. " * 10     # ~60 chars
    para2 = "두 번째 단락. " * 10  # ~70 chars
    para3 = "세 번째 단락. " * 10
    text = "\n\n".join([para1, para2, para3])
    chunks = Chunker(chunk_size=200, overlap=30).chunk(text)
    # 각 청크가 단락 중간에서 잘리지 않았는지 확인
    for chunk in chunks:
        assert chunk == chunk.strip()


def test_single_paragraph_exceeding_chunk_size_is_hard_split():
    long_para = "X" * 1000
    chunks = Chunker(chunk_size=300, overlap=50).chunk(long_para)
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk) <= 300
