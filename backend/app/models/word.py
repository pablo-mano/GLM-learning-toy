import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean, UniqueConstraint, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
from app.core.constants import DifficultyLevel, LanguageCode


class Word(Base):
    __tablename__ = "words"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id = Column(UUID(as_uuid=True), ForeignKey("domains.id", ondelete="CASCADE"), nullable=False)
    difficulty = Column(String(20), nullable=False, default=DifficultyLevel.BEGINNER)
    image_url = Column(String(500), nullable=True)
    audio_url = Column(String(500), nullable=True)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    domain = relationship("Domain", back_populates="words")
    translations = relationship("WordTranslation", back_populates="word", cascade="all, delete-orphan")
    prerequisites = relationship(
        "WordPrerequisite",
        foreign_keys="WordPrerequisite.word_id",
        back_populates="word",
        cascade="all, delete-orphan"
    )
    dependent_words = relationship(
        "WordPrerequisite",
        foreign_keys="WordPrerequisite.prerequisite_id",
        back_populates="prerequisite",
        cascade="all, delete-orphan"
    )


class WordTranslation(Base):
    __tablename__ = "word_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    word_id = Column(UUID(as_uuid=True), ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    language = Column(String(5), nullable=False)
    text = Column(String(200), nullable=False)
    phonetic = Column(String(500), nullable=True)
    example_sentence = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    word = relationship("Word", back_populates="translations")

    __table_args__ = (
        UniqueConstraint("word_id", "language", name="uq_word_language"),
    )


class WordPrerequisite(Base):
    __tablename__ = "word_prerequisites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    word_id = Column(UUID(as_uuid=True), ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    prerequisite_id = Column(UUID(as_uuid=True), ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    word = relationship("Word", foreign_keys=[word_id], back_populates="prerequisites")
    prerequisite = relationship("Word", foreign_keys=[prerequisite_id], back_populates="dependent_words")

    __table_args__ = (
        UniqueConstraint("word_id", "prerequisite_id", name="uq_word_prerequisite"),
    )
