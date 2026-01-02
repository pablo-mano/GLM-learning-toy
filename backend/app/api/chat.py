import uuid
import random
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.user import User
from app.models.progress import Child
from app.models.chat import ChatSession, ChatMessage
from app.models.word import Word
from app.schemas.chat import ChatRequest, ChatResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatService:
    """Mock AI chat service for MVP."""

    RESPONSES = {
        "greeting": [
            "Hello! Let's learn some words together!",
            "Hi! What would you like to learn today?",
            "Welcome back! Ready to practice?"
        ],
        "encouragement": [
            "Great job! You're doing amazing!",
            "Wonderful! Keep it up!",
            "You're so smart!"
        ],
        "hint": [
            "Here's a hint: think about what we learned before!",
            "Take your time, you've got this!",
            "Try to remember the words we practiced!"
        ],
        "default": [
            "That's interesting! Let's keep learning!",
            "Nice! Would you like to practice more words?",
            "Great! Let's continue our adventure!"
        ]
    }

    @classmethod
    def get_response(cls, message: str, context: dict = None) -> str:
        """Get mock AI response based on message content."""
        message_lower = message.lower()

        if any(word in message_lower for word in ["hello", "hi", "hey"]):
            return random.choice(cls.RESPONSES["greeting"])
        elif any(word in message_lower for word in ["help", "stuck", "hint", "don't know"]):
            return random.choice(cls.RESPONSES["hint"])
        elif any(word in message_lower for word in ["good", "great", "easy"]):
            return random.choice(cls.RESPONSES["encouragement"])

        return random.choice(cls.RESPONSES["default"])


@router.post("/message", response_model=ChatResponse)
async def send_message(
    chat_data: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Send a message and get AI response."""
    # Verify child
    child_result = await db.execute(
        select(Child).where(Child.id == chat_data.child_id, Child.user_id == current_user.id)
    )
    child = child_result.scalar_one_or_none()

    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )

    # Get or create session
    if chat_data.session_id:
        session_result = await db.execute(
            select(ChatSession).where(
                ChatSession.id == chat_data.session_id,
                ChatSession.child_id == chat_data.child_id
            )
        )
        session = session_result.scalar_one_or_none()

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
    else:
        session = ChatSession(
            child_id=chat_data.child_id,
            domain_id=chat_data.domain_id
        )
        db.add(session)
        await db.flush()

    # Create user message
    user_message = ChatMessage(
        session_id=session.id,
        role="user",
        content=chat_data.message,
        word_id=None
    )
    db.add(user_message)

    # Get AI response
    ai_response_text = ChatService.get_response(
        chat_data.message,
        {"domain_id": str(chat_data.domain_id) if chat_data.domain_id else None}
    )

    # Create assistant message
    assistant_message = ChatMessage(
        session_id=session.id,
        role="assistant",
        content=ai_response_text,
        word_id=None
    )
    db.add(assistant_message)

    # Update session
    session.message_count += 2

    await db.commit()
    await db.refresh(assistant_message)

    return ChatResponse(
        session_id=session.id,
        message={
            "role": "assistant",
            "content": assistant_message.content,
            "word_id": None,
            "timestamp": assistant_message.created_at
        }
    )


@router.get("/sessions/{session_id}/history")
async def get_chat_history(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get message history for a session."""
    # Verify session belongs to user's child
    session_result = await db.execute(
        select(ChatSession)
        .join(Child)
        .join(User)
        .where(
            ChatSession.id == session_id,
            User.id == current_user.id
        )
    )
    session = session_result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    # Get messages
    messages_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
    )
    messages = messages_result.scalars().all()

    return {
        "session_id": str(session.id),
        "child_id": str(session.child_id),
        "messages": [
            {
                "id": str(m.id),
                "role": m.role,
                "content": m.content,
                "word_id": str(m.word_id) if m.word_id else None,
                "timestamp": m.created_at
            }
            for m in messages
        ]
    }
