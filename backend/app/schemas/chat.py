import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str
    word_id: Optional[uuid.UUID] = None
    timestamp: datetime


class ChatRequest(BaseModel):
    session_id: Optional[uuid.UUID] = None
    child_id: uuid.UUID
    message: str
    domain_id: Optional[uuid.UUID] = None


class ChatResponse(BaseModel):
    session_id: uuid.UUID
    message: ChatMessage
