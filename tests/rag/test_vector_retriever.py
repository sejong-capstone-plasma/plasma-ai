import pytest

from app.rag.chunker import Chunker
from app.rag.index_builder import IndexBuilder
from app.rag.vector_retriever import VectorRetriever


@pytest.fixture
def built_index(tmp_path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "overview.md").write_text(
        "# 플랫폼 개요\n\n"
        "ion flux는 단위 면적·시간당 이온 수입니다.\n\n"
        "bias power가 높을수록 이온 에너지가 증가합니다.\n\n"
        "pressure가 낮을수록 전자 온도가 높아집니다.",
        encoding="utf-8",
    )
    index_dir = tmp_path / "chroma"
    IndexBuilder(
        docs_dir=docs_dir,
        index_dir=index_dir,
        collection_name="test",
        chunker=Chunker(chunk_size=500, overlap=50),
    ).build()
    return index_dir


@pytest.fixture
def retriever(built_index):
    return VectorRetriever(
        index_dir=str(built_index),
        collection_name="test",
        top_k=3,
    )


@pytest.mark.asyncio
async def test_retrieve_returns_results(retriever):
    results = await retriever.retrieve("ion flux가 뭐야?")
    assert len(results) > 0


@pytest.mark.asyncio
async def test_result_has_required_fields(retriever):
    results = await retriever.retrieve("bias power")
    doc = results[0]
    assert doc.title
    assert doc.chunk
    assert 0.0 <= doc.score <= 1.0
    assert doc.metadata.source


@pytest.mark.asyncio
async def test_top_k_limits_results(built_index):
    retriever = VectorRetriever(index_dir=str(built_index), collection_name="test", top_k=1)
    results = await retriever.retrieve("pressure")
    assert len(results) == 1


@pytest.mark.asyncio
async def test_collection_lazy_loaded(retriever):
    assert retriever._collection is None
    await retriever.retrieve("test")
    assert retriever._collection is not None
