import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class DomainBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None


class DomainCreate(DomainBase):
    pass


class DomainUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None


class DomainResponse(DomainBase):
    id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    is_system: bool
    word_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class WordTranslationBase(BaseModel):
    language: str
    text: str = Field(..., min_length=1, max_length=200)
    phonetic: Optional[str] = None
    example_sentence: Optional[str] = None


class WordTranslationResponse(WordTranslationBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class WordBase(BaseModel):
    domain_id: uuid.UUID
    difficulty: str = "beginner"
    image_url: Optional[str] = None
    sort_order: int = 0


class WordCreate(WordBase):
    translations: list[WordTranslationBase]
    prerequisite_ids: list[uuid.UUID] = []


class WordUpdate(BaseModel):
    difficulty: Optional[str] = None
    image_url: Optional[str] = None
    sort_order: Optional[int] = None
    translations: Optional[list[WordTranslationBase]] = None


class WordResponse(WordBase):
    id: uuid.UUID
    translations: list[WordTranslationResponse]
    prerequisite_ids: list[uuid.UUID]
    created_at: datetime

    class Config:
        from_attributes = True
