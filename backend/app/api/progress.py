import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.user import User
from app.models.progress import Child, Progress
from app.models.word import Word, WordTranslation, WordPrerequisite
from app.schemas.progress import ProgressResponse, ProgressAttempt, DomainProgressResponse, NextWordsResponse, WordProgressResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.get("/child/{child_id}", response_model=list[ProgressResponse])
async def get_child_progress(
    child_id: uuid.UUID,
    domain_id: Optional[uuid.UUID] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all progress for a child."""
    # Verify child belongs to user
    child_result = await db.execute(
        select(Child).where(Child.id == child_id, Child.user_id == current_user.id)
    )
    child = child_result.scalar_one_or_none()

    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )

    # Build query
    query = select(Progress).where(Progress.child_id == child_id)

    if domain_id:
        # Join with words to filter by domain
        query = query.join(Word).where(Word.domain_id == domain_id)

    result = await db.execute(query)
    progress_records = result.scalars().all()

    return [
        ProgressResponse(
            id=p.id,
            word_id=p.word_id,
            status=p.status,
            attempts=p.attempts,
            correct_count=p.correct_count,
            streak_count=p.streak_count,
            accuracy=round(p.correct_count / p.attempts, 2) if p.attempts > 0 else 0.0,
            last_practiced_at=p.last_practiced_at,
            mastered_at=p.mastered_at
        )
        for p in progress_records
    ]


@router.get("/child/{child_id}/overview")
async def get_progress_overview(
    child_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get overview statistics for a child."""
    # Verify child
    child_result = await db.execute(
        select(Child).where(Child.id == child_id, Child.user_id == current_user.id)
    )
    child = child_result.scalar_one_or_none()

    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )

    # Get progress counts
    result = await db.execute(select(Progress).where(Progress.child_id == child_id))
    all_progress = result.scalars().all()

    stats = {
        "total_words": len(all_progress),
        "mastered": sum(1 for p in all_progress if p.status == "mastered"),
        "practicing": sum(1 for p in all_progress if p.status == "practicing"),
        "in_progress": sum(1 for p in all_progress if p.status == "in_progress"),
        "unlocked": sum(1 for p in all_progress if p.status == "unlocked"),
        "locked": sum(1 for p in all_progress if p.status == "locked"),
        "total_attempts": sum(p.attempts for p in all_progress),
        "total_correct": sum(p.correct_count for p in all_progress)
    }

    stats["accuracy"] = round(
        stats["total_correct"] / stats["total_attempts"], 2
    ) if stats["total_attempts"] > 0 else 0.0

    return stats


@router.get("/child/{child_id}/next-words", response_model=NextWordsResponse)
async def get_next_words(
    child_id: uuid.UUID,
    domain_id: uuid.UUID,
    limit: int = 5,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get recommended next words for a child to learn."""
    # Verify child
    child_result = await db.execute(
        select(Child).where(Child.id == child_id, Child.user_id == current_user.id)
    )
    child = child_result.scalar_one_or_none()

    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )

    # Get all words in domain with translations
    words_result = await db.execute(
        select(Word)
        .options(selectinload(Word.translations))
        .where(Word.domain_id == domain_id, Word.is_active == True)
    )
    words = words_result.scalars().all()

    # Get current progress for child
    progress_result = await db.execute(
        select(Progress).where(Progress.child_id == child_id)
    )
    progress_records = progress_result.scalars().all()

    # Build mastered set and progress map
    mastered = set()
    progress_map = {}
    for p in progress_records:
        progress_map[p.word_id] = p
        if p.status == "mastered":
            mastered.add(p.word_id)

    # Get all prerequisites
    word_ids = [w.id for w in words]
    prereq_result = await db.execute(
        select(WordPrerequisite.word_id, WordPrerequisite.prerequisite_id)
        .where(WordPrerequisite.word_id.in_(word_ids))
    )
    prereq_map = {}
    for word_id, prereq_id in prereq_result.all():
        if word_id not in prereq_map:
            prereq_map[word_id] = []
        prereq_map[word_id].append(prereq_id)

    # Find unlocked words (prerequisites met, not mastered)
    candidates = []
    for word in words:
        if word.id in mastered:
            continue

        # Check if prerequisites are met
        prereqs = prereq_map.get(word.id, [])
        if all(p in mastered for p in prereqs):
            # Calculate priority score
            difficulty_score = {"beginner": 100, "intermediate": 50, "advanced": 10}
            score = difficulty_score.get(word.difficulty, 0)

            # Bonus for unlocking many words
            unlock_count = sum(1 for wid, pr in prereq_map.items() if word.id in pr)
            score += unlock_count * 10

            candidates.append((word, score))

    # Sort by score and limit
    candidates.sort(key=lambda x: x[1], reverse=True)
    selected_words = candidates[:limit]

    # Build response
    response_words = []
    for word, _ in selected_words:
        progress = progress_map.get(word.id)
        status = progress.status if progress else "unlocked"

        translations_dict = {t.language: t.text for t in word.translations}

        response_words.append(WordProgressResponse(
            word_id=word.id,
            word_text=translations_dict,
            status=status,
            difficulty=word.difficulty
        ))

    return NextWordsResponse(words=response_words)


@router.post("/child/{child_id}/word/{word_id}/attempt", response_model=ProgressResponse)
async def record_attempt(
    child_id: uuid.UUID,
    word_id: uuid.UUID,
    attempt_data: ProgressAttempt,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Record a practice attempt for a word."""
    # Verify child
    child_result = await db.execute(
        select(Child).where(Child.id == child_id, Child.user_id == current_user.id)
    )
    child = child_result.scalar_one_or_none()

    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )

    # Get or create progress record
    result = await db.execute(
        select(Progress).where(
            Progress.child_id == child_id,
            Progress.word_id == word_id
        )
    )
    progress = result.scalar_one_or_none()

    if not progress:
        progress = Progress(
            child_id=child_id,
            word_id=word_id,
            status="unlocked"
        )
        db.add(progress)

    # Update attempt stats
    progress.attempts += 1
    if attempt_data.correct:
        progress.correct_count += 1
        progress.streak_count += 1
    else:
        progress.streak_count = 0

    progress.last_practiced_at = datetime.utcnow()

    # Calculate new status
    if progress.attempts >= 3:
        accuracy = progress.correct_count / progress.attempts
        if accuracy >= 0.8:
            progress.status = "mastered"
            if not progress.mastered_at:
                progress.mastered_at = datetime.utcnow()
        elif accuracy >= 0.6 and progress.streak_count >= 2:
            progress.status = "practicing"
        else:
            progress.status = "in_progress"
    else:
        progress.status = "in_progress"

    await db.commit()
    await db.refresh(progress)

    return ProgressResponse(
        id=progress.id,
        word_id=progress.word_id,
        status=progress.status,
        attempts=progress.attempts,
        correct_count=progress.correct_count,
        streak_count=progress.streak_count,
        accuracy=round(progress.correct_count / progress.attempts, 2) if progress.attempts > 0 else 0.0,
        last_practiced_at=progress.last_practiced_at,
        mastered_at=progress.mastered_at
    )
