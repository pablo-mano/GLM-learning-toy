import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProgressBase(BaseModel):
    word_id: uuid.UUID
    correct: bool


class ProgressAttempt(BaseModel):
    correct: bool


class ProgressResponse(BaseModel):
    id: uuid.UUID
    word_id: uuid.UUID
    status: str
    attempts: int
    correct_count: int
    streak_count: int
    accuracy: float
    last_practiced_at: Optional[datetime]
    mastered_at: Optional[datetime]

    class Config:
        from_attributes = True


class WordProgressResponse(BaseModel):
    word_id: uuid.UUID
    word_text: dict[str, str]  # language -> text
    status: str
    difficulty: str


class DomainProgressResponse(BaseModel):
    domain_id: uuid.UUID
    domain_name: str
    total_words: int
    mastered_words: int
    in_progress_words: int
    unlocked_words: int
    locked_words: int


class NextWordsResponse(BaseModel):
    words: list[WordProgressResponse]
