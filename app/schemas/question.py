from typing import List, Optional

from pydantic import Field

from app.schemas.common import CommonBaseModel
from app.schemas.extract import ChatMessage


class SourceMetadata(CommonBaseModel):
    source: str = Field(..., description="File path or URL of the source document")
    section: Optional[str] = Field(default=None, description="Section or heading within the document")
    page: Optional[int] = Field(default=None, description="Page number (for PDFs)")
    author: Optional[str] = Field(default=None, description="Author(s) of the document")
    year: Optional[int] = Field(default=None, description="Publication year")
    doi: Optional[str] = Field(default=None, description="DOI (for academic papers)")


class SourceDocument(CommonBaseModel):
    title: str = Field(..., description="Document title")
    chunk: str = Field(..., description="Retrieved text passage")
    score: float = Field(..., description="Relevance score (0–1)")
    metadata: SourceMetadata


class QuestionPipelineRequest(CommonBaseModel):
    request_id: str = Field(..., description="Request identifier")
    original_user_input: str = Field(..., description="Original user input text")
    history: List[ChatMessage] = Field(default_factory=list, description="Conversation history")


class QuestionPipelineResponse(CommonBaseModel):
    request_id: str
    answer: str
    sources: List[SourceDocument] = Field(default_factory=list, description="Retrieved source documents")
