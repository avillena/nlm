"""Pydantic models for request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class NotebookCreate(BaseModel):
    """Request model for creating a notebook."""

    title: str = Field(..., min_length=1, max_length=200)
    emoji: Optional[str] = Field(None, max_length=10)


class NotebookResponse(BaseModel):
    """Response model for notebook data."""

    project_id: str
    title: str
    emoji: Optional[str] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    source_count: int = 0


class SourceAdd(BaseModel):
    """Request model for adding a source."""

    source_input: str = Field(..., min_length=1)
    source_type: Literal["url", "file", "text"] = "url"
    mime_type: Optional[str] = None


class SourceResponse(BaseModel):
    """Response model for source data."""

    source_id: str
    title: str
    source_type: str
    added_at: Optional[datetime] = None
    status: Optional[str] = None


class AudioCreate(BaseModel):
    """Request model for creating audio overview."""

    instructions: str = Field(
        default="Provide a comprehensive overview",
        max_length=500,
    )


class AudioResponse(BaseModel):
    """Response model for audio overview."""

    audio_id: str
    status: Literal["pending", "processing", "ready", "failed"]
    duration: Optional[int] = None  # seconds
    url: Optional[str] = None
    size_bytes: Optional[int] = None


class NoteCreate(BaseModel):
    """Request model for creating a note."""

    title: str = Field(..., min_length=1, max_length=200)


class NoteUpdate(BaseModel):
    """Request model for updating a note."""

    content: str
    title: str = Field(..., min_length=1, max_length=200)


class NoteResponse(BaseModel):
    """Response model for note data."""

    note_id: str
    title: str
    content: Optional[str] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None


class GenerationRequest(BaseModel):
    """Request model for content generation."""

    notebook_id: str


class ErrorResponse(BaseModel):
    """Response model for errors."""

    error: str
    detail: Optional[str] = None
