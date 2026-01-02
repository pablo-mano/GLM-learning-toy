import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.user import User
from app.models.domain import Domain
from app.models.word import Word, WordTranslation, WordPrerequisite
from app.schemas.domain import DomainCreate, DomainResponse, DomainUpdate, WordCreate, WordResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/domains", tags=["Domains"])


@router.get("", response_model=list[DomainResponse])
async def list_domains(
    include_system: bool = True,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all domains (system + user's custom domains)."""
    query = select(Domain)

    if include_system:
        query = query.where((Domain.user_id == current_user.id) | (Domain.is_system == True))
    else:
        query = query.where(Domain.user_id == current_user.id)

    result = await db.execute(query)
    domains = result.scalars().all()

    # Add word count for each domain
    response = []
    for domain in domains:
        word_count_result = await db.execute(
            select(func.count()).select_from(Word).where(Word.domain_id == domain.id)
        )
        word_count = word_count_result.scalar() or 0

        response.append(DomainResponse(
            id=domain.id,
            user_id=domain.user_id,
            name=domain.name,
            description=domain.description,
            icon=domain.icon,
            color=domain.color,
            is_system=domain.is_system,
            word_count=word_count,
            created_at=domain.created_at
        ))

    return response


@router.post("", response_model=DomainResponse, status_code=status.HTTP_201_CREATED)
async def create_domain(
    domain_data: DomainCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a custom domain."""
    new_domain = Domain(
        user_id=current_user.id,
        name=domain_data.name,
        description=domain_data.description,
        icon=domain_data.icon,
        color=domain_data.color,
        is_system=False
    )

    db.add(new_domain)
    await db.commit()
    await db.refresh(new_domain)

    return DomainResponse(
        id=new_domain.id,
        user_id=new_domain.user_id,
        name=new_domain.name,
        description=new_domain.description,
        icon=new_domain.icon,
        color=new_domain.color,
        is_system=new_domain.is_system,
        word_count=0,
        created_at=new_domain.created_at
    )


@router.get("/{domain_id}", response_model=DomainResponse)
async def get_domain(
    domain_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get domain details."""
    result = await db.execute(
        select(Domain).where(
            (Domain.id == domain_id) &
            ((Domain.user_id == current_user.id) | (Domain.is_system == True))
        )
    )
    domain = result.scalar_one_or_none()

    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found"
        )

    word_count_result = await db.execute(
        select(func.count()).select_from(Word).where(Word.domain_id == domain.id)
    )
    word_count = word_count_result.scalar() or 0

    return DomainResponse(
        id=domain.id,
        user_id=domain.user_id,
        name=domain.name,
        description=domain.description,
        icon=domain.icon,
        color=domain.color,
        is_system=domain.is_system,
        word_count=word_count,
        created_at=domain.created_at
    )


@router.post("/{domain_id}/words", response_model=WordResponse, status_code=status.HTTP_201_CREATED)
async def create_word(
    domain_id: uuid.UUID,
    word_data: WordCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new word in a domain."""
    # Verify domain exists and user has access
    domain_result = await db.execute(
        select(Domain).where(
            (Domain.id == domain_id) &
            ((Domain.user_id == current_user.id) | (Domain.is_system == True))
        )
    )
    domain = domain_result.scalar_one_or_none()

    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found"
        )

    # Create word
    new_word = Word(
        domain_id=domain_id,
        difficulty=word_data.difficulty,
        image_url=word_data.image_url,
        sort_order=word_data.sort_order
    )
    db.add(new_word)
    await db.flush()  # Get the ID

    # Create translations
    for trans_data in word_data.translations:
        translation = WordTranslation(
            word_id=new_word.id,
            language=trans_data.language,
            text=trans_data.text,
            phonetic=trans_data.phonetic,
            example_sentence=trans_data.example_sentence
        )
        db.add(translation)

    # Create prerequisites
    for prereq_id in word_data.prerequisite_ids:
        prerequisite = WordPrerequisite(
            word_id=new_word.id,
            prerequisite_id=prereq_id
        )
        db.add(prerequisite)

    await db.commit()
    await db.refresh(new_word)

    # Load relationships for response
    result = await db.execute(
        select(Word)
        .options(selectinload(Word.translations))
        .where(Word.id == new_word.id)
    )
    word = result.scalar_one()

    # Get prerequisite IDs
    prereq_result = await db.execute(
        select(WordPrerequisite.prerequisite_id).where(WordPrerequisite.word_id == word.id)
    )
    prereq_ids = [row[0] for row in prereq_result.all()]

    return WordResponse(
        id=word.id,
        domain_id=word.domain_id,
        difficulty=word.difficulty,
        image_url=word.image_url,
        sort_order=word.sort_order,
        translations=[
            {
                "id": t.id,
                "language": t.language,
                "text": t.text,
                "phonetic": t.phonetic,
                "example_sentence": t.example_sentence
            }
            for t in word.translations
        ],
        prerequisite_ids=prereq_ids,
        created_at=word.created_at
    )


@router.get("/{domain_id}/words")
async def list_domain_words(
    domain_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all words in a domain."""
    # Verify domain access
    domain_result = await db.execute(
        select(Domain).where(
            (Domain.id == domain_id) &
            ((Domain.user_id == current_user.id) | (Domain.is_system == True))
        )
    )
    domain = domain_result.scalar_one_or_none()

    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found"
        )

    result = await db.execute(
        select(Word)
        .options(selectinload(Word.translations))
        .where(Word.domain_id == domain_id)
        .order_by(Word.sort_order)
    )
    words = result.scalars().all()

    # Get prerequisite IDs for each word
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

    return [
        {
            "id": w.id,
            "domain_id": w.domain_id,
            "difficulty": w.difficulty,
            "image_url": w.image_url,
            "sort_order": w.sort_order,
            "translations": [
                {
                    "id": t.id,
                    "language": t.language,
                    "text": t.text,
                    "phonetic": t.phonetic,
                    "example_sentence": t.example_sentence
                }
                for t in w.translations
            ],
            "prerequisite_ids": prereq_map.get(w.id, []),
            "created_at": w.created_at
        }
        for w in words
    ]


@router.get("/{domain_id}/graph")
async def get_domain_graph(
    domain_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get learning graph for a domain."""
    # Verify domain access
    domain_result = await db.execute(
        select(Domain).where(
            (Domain.id == domain_id) &
            ((Domain.user_id == current_user.id) | (Domain.is_system == True))
        )
    )
    domain = domain_result.scalar_one_or_none()

    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found"
        )

    # Get words with translations
    result = await db.execute(
        select(Word)
        .options(selectinload(Word.translations))
        .where(Word.domain_id == domain_id)
        .order_by(Word.sort_order)
    )
    words = result.scalars().all()

    # Get all prerequisite relationships
    word_ids = [w.id for w in words]
    prereq_result = await db.execute(
        select(WordPrerequisite.word_id, WordPrerequisite.prerequisite_id)
        .where(WordPrerequisite.word_id.in_(word_ids))
    )
    edges = [
        {"from": str(prereq_id), "to": str(word_id)}
        for word_id, prereq_id in prereq_result.all()
    ]

    # Build nodes
    nodes = []
    for w in words:
        translations_dict = {t.language: t.text for t in w.translations}
        nodes.append({
            "id": str(w.id),
            "domain_id": str(w.domain_id),
            "difficulty": w.difficulty,
            "image_url": w.image_url,
            "translations": translations_dict,
            "sort_order": w.sort_order
        })

    # Compute depth levels (topological sort approximation)
    depth_map = {}
    for w in words:
        depth_map[w.id] = 0

    # Simple BFS to compute depths
    changed = True
    iterations = 0
    while changed and iterations < len(word_ids) + 1:
        changed = False
        iterations += 1
        for word_id, prereq_id in prereq_result.all():
            if depth_map.get(prereq_id, 0) + 1 > depth_map.get(word_id, 0):
                depth_map[word_id] = depth_map.get(prereq_id, 0) + 1
                changed = True

    # Group by depth
    levels = {}
    for word_id, depth in depth_map.items():
        if depth not in levels:
            levels[depth] = []
        levels[depth].append(str(word_id))

    return {
        "domain_id": str(domain.id),
        "domain_name": domain.name,
        "nodes": nodes,
        "edges": edges,
        "levels": [levels.get(d, []) for d in range(max(levels.keys()) + 1) if levels]
    }
