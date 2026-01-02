import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, DateTime, Date, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
from app.core.constants import ProgressStatus


class Child(Base):
    __tablename__ = "children"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    preferred_language = Column(String(5), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="children")
    progress = relationship("Progress", back_populates="child", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="child", cascade="all, delete-orphan")


class Progress(Base):
    __tablename__ = "progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    child_id = Column(UUID(as_uuid=True), ForeignKey("children.id", ondelete="CASCADE"), nullable=False)
    word_id = Column(UUID(as_uuid=True), ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    status = Column(SQLEnum(ProgressStatus), nullable=False, default=ProgressStatus.LOCKED)
    attempts = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    streak_count = Column(Integer, default=0)
    last_practiced_at = Column(DateTime, nullable=True)
    unlocked_at = Column(DateTime, nullable=True)
    mastered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    child = relationship("Child", back_populates="progress")
    word = relationship("Word")
