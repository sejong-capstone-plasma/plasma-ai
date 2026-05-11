import pytest

from app.rag.chunker import Chunker
from app.rag.index_builder import IndexBuilder


@pytest.fixture
def docs_dir(tmp_path):
    md = tmp_path / "overview.md"
    md.write_text("# 플랫폼 개요\n\nion flux는 cm⁻²s⁻¹ 단위입니다.\n\nbias power가 높을수록 이온 에너지가 증가합니다.", encoding="utf-8")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "note.md").write_text("# 서브 문서\n\n추가 설명입니다.", encoding="utf-8")
    return tmp_path


@pytest.fixture
def builder(docs_dir, tmp_path):
    return IndexBuilder(
        docs_dir=docs_dir,
        index_dir=tmp_path / "chroma",
        collection_name="test_collection",
        chunker=Chunker(chunk_size=500, overlap=50),
    )


def test_build_creates_index_dir(builder, tmp_path):
    builder.build()
    assert (tmp_path / "chroma").exists()


def test_build_indexes_all_md_files(builder):
    builder.build()
    import chromadb
    client = chromadb.PersistentClient(path=str(builder.index_dir))
    collection = client.get_collection("test_collection")
    assert collection.count() > 0


def test_chunk_ids_include_filename(builder):
    builder.build()
    import chromadb
    client = chromadb.PersistentClient(path=str(builder.index_dir))
    collection = client.get_collection("test_collection")
    results = collection.get()
    assert any("overview.md" in id_ for id_ in results["ids"])


def test_metadata_contains_source_and_title(builder):
    builder.build()
    import chromadb
    client = chromadb.PersistentClient(path=str(builder.index_dir))
    collection = client.get_collection("test_collection")
    results = collection.get(include=["metadatas"])
    meta = results["metadatas"][0]
    assert "source" in meta
    assert "title" in meta
    assert "chunk_index" in meta


def test_empty_document_is_skipped(docs_dir, tmp_path):
    (docs_dir / "empty.md").write_text("", encoding="utf-8")
    builder = IndexBuilder(
        docs_dir=docs_dir,
        index_dir=tmp_path / "chroma",
        collection_name="test_collection",
        chunker=Chunker(),
    )
    builder.build()
    import chromadb
    client = chromadb.PersistentClient(path=str(builder.index_dir))
    collection = client.get_collection("test_collection")
    results = collection.get()
    assert not any("empty.md" in id_ for id_ in results["ids"])


def test_rebuild_resets_collection(builder):
    builder.build()
    builder.build()
    import chromadb
    client = chromadb.PersistentClient(path=str(builder.index_dir))
    collection = client.get_collection("test_collection")
    # 두 번 빌드해도 중복 없이 동일한 수의 청크
    first_count = collection.count()
    assert first_count > 0

    builder.build()
    client2 = chromadb.PersistentClient(path=str(builder.index_dir))
    collection2 = client2.get_collection("test_collection")
    assert collection2.count() == first_count
