# LearningToy Architecture

This document describes the system architecture, data models, and core algorithms of LearningToy.

## System Overview

LearningToy follows a client-server architecture with a React frontend and FastAPI backend, communicating via REST API over HTTP.

```
┌─────────────────────────────────────────────────────────────────────┐
│                           Frontend (React)                          │
│  ┌──────────────────────┐              ┌───────────────────────┐   │
│  │  Device Emulator     │              │  Parent Dashboard     │   │
│  │  (Child Interface)   │              │  (Admin Interface)    │   │
│  └──────────────────────┘              └───────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                                 │ HTTP/REST + JWT
                                 │
┌─────────────────────────────────────────────────────────────────────┐
│                          Backend (FastAPI)                          │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────────┐  │
│  │   Auth    │  │  Domains  │  │ Progress  │  │     Chat      │  │
│  │   API     │  │   API     │  │   API     │  │     API       │  │
│  └───────────┘  └───────────┘  └───────────┘  └───────────────┘  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                  Services Layer (Business Logic)             │  │
│  │  LearningService │ GraphService │ ProgressService │ ChatService│
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                                 │ SQLAlchemy Async
                                 │
┌─────────────────────────────────────────────────────────────────────┐
│                        PostgreSQL Database                          │
└─────────────────────────────────────────────────────────────────────┘
```

## Frontend Architecture

### Component Structure

```
src/
├── components/
│   ├── DeviceEmulator/           # Child-facing learning interface
│   │   ├── DeviceFrame.tsx       # Physical device frame styling
│   │   ├── DeviceScreen.tsx      # Main screen with routing
│   │   ├── WordCard.tsx          # Word display with animations
│   │   └── ChatInterface.tsx     # AI tutor chat
│   │
│   └── ParentDashboard/          # Parent admin interface
│       ├── DomainGraph.tsx       # ReactFlow graph visualization
│       ├── ProgressOverview.tsx  # Statistics and charts
│       └── DomainEditor.tsx      # CRUD for domains/words
│
├── stores/                       # Zustand state management
│   ├── authStore.ts              # User authentication state
│   ├── deviceStore.ts            # Device emulator state
│   └── domainStore.ts            # Domains and words cache
│
├── services/                     # API client layer
│   └── api.ts                    # Axios/Fetch wrapper
│
└── types/                        # TypeScript definitions
    └── index.ts                  # Shared interfaces
```

### State Management

LearningToy uses **Zustand** for lightweight state management:

```typescript
// authStore.ts - Authentication state
interface AuthState {
  user: User | null;
  token: string | null;
  children: Child[];
  login: (email, password) => Promise<void>;
  logout: () => void;
}

// deviceStore.ts - Device emulator state
interface DeviceState {
  currentWord: Word | null;
  mode: 'learning' | 'practicing' | 'chat';
  chatHistory: Message[];
  submitAttempt: (correct: boolean) => Promise<void>;
}

// domainStore.ts - Domain data cache
interface DomainState {
  domains: Domain[];
  selectedDomain: Domain | null;
  fetchDomains: () => Promise<void>;
}
```

## Backend Architecture

### Layer Structure

```
app/
├── api/                          # Route handlers (thin layer)
│   ├── auth.py                  # Auth endpoints
│   ├── domains.py               # Domain/word CRUD
│   ├── progress.py              # Progress tracking
│   └── chat.py                  # Chat endpoints
│
├── services/                     # Business logic
│   ├── auth_service.py          # JWT token management
│   ├── learning_service.py      # Learning algorithm
│   ├── graph_service.py         # DAG operations
│   └── chat_service.py          # AI chat logic
│
├── models/                       # SQLAlchemy ORM
│   ├── user.py                  # User, Child models
│   ├── domain.py                # Domain model
│   ├── word.py                  # Word, WordTranslation, Prerequisite
│   └── progress.py              # Progress, ChatSession
│
├── schemas/                      # Pydantic validation
│   ├── auth.py
│   ├── domain.py
│   └── progress.py
│
└── core/
    ├── security.py              # Password hashing, JWT
    └── constants.py             # Enums, config
```

### API Layer Design

Route handlers are thin - they validate input and delegate to services:

```python
# api/progress.py
@router.get("/child/{child_id}/next-words")
async def get_next_words(child_id: int, limit: int = 5):
    # Validate ownership
    child = await authorize_child(child_id)

    # Delegate to service
    words = await learning_service.get_next_words(child_id, limit)

    return {"words": words}
```

## Database Schema

### Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────┐
│    users    │       │  children   │
├─────────────┤       ├─────────────┤
│ id (PK)     │──┐    │ id (PK)     │
│ email       │  └────│ parent_id   │
│ password    │       │ name        │
│ created_at  │       │ language    │
└─────────────┘       └─────────────┘
                              │
                              │ learns
                              │
┌─────────────┐       ┌─────────────┐       ┌─────────────────────┐
│  domains    │       │   words     │       │ word_translations   │
├─────────────┤       ├─────────────┤       ├─────────────────────┤
│ id (PK)     │──┐    │ id (PK)     │──┐    │ id (PK)             │
│ name        │  └────│ domain_id   │  └────│ word_id             │
│ description │       │ difficulty  │       │ language            │
└─────────────┘       │ enabled     │       │ text                │
                      └─────────────┘       │ phonetic           │
                              │             └─────────────────────┘
                              │ requires
                              │
                      ┌───────────────┐
                      │  progress     │
                      ├───────────────┤
                      │ child_id (PK) │
                      │ word_id (PK)  │
                      │ status        │
                      │ attempts      │
                      │ last_attempt  │
                      └───────────────┘
```

### Key Tables

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `users` | Parent accounts | `id`, `email`, `password_hash` |
| `children` | Child profiles | `id`, `parent_id`, `name`, `language` |
| `domains` | Learning domains | `id`, `name`, `description` |
| `words` | Vocabulary items | `id`, `domain_id`, `difficulty`, `enabled` |
| `word_translations` | Multilingual text | `word_id`, `language`, `text`, `phonetic` |
| `word_prerequisites` | Learning graph edges | `word_id`, `prerequisite_id` |
| `progress` | Learning progress | `child_id`, `word_id`, `status`, `attempts` |

### Progress Status States

```
┌─────────┐    prerequisites met    ┌───────────┐
│ locked  │ ──────────────────────> │ unlocked  │
└─────────┘                         └───────────┘
                                             │
                                    first attempt
                                             │
                                             v
┌───────────┐    practice needed    ┌─────────────┐
│ practiced │ <─────────────────── │ in_progress │
└───────────┘                      └─────────────┘
     │                                   │
     │ 3+ successful attempts             │ single attempt
     │                                   │
     v                                   v
┌───────────┐                       ┌───────────┐
│ mastered  │ <──────────────────── │ practiced │
└───────────┘    successful         └───────────┘
```

| Status | Description | Transition Condition |
|--------|-------------|---------------------|
| `locked` | Prerequisites not met | All prerequisites mastered |
| `unlocked` | Ready to learn | First practice attempt |
| `in_progress` | Currently learning | Any practice attempt |
| `practicing` | Needs more practice | 3+ successful attempts |
| `mastered` | Successfully learned | - |

## Learning Graph Algorithm

### Directed Acyclic Graph (DAG) Structure

The learning graph is a DAG where:
- **Nodes** = Words (with metadata: difficulty, domain, translations)
- **Edges** = Prerequisite relationships (A must be learned before B)

### Properties

1. **Acyclic**: No word can directly or indirectly require itself
2. **Progressive**: Words unlock as prerequisites are mastered
3. **Multi-path**: A word may have multiple prerequisite paths

### Next Word Recommendation Algorithm

```python
async def get_next_words(child_id: int, limit: int = 5) -> List[Word]:
    """
    Get recommended next words for a child.

    Algorithm:
    1. Get all mastered words for the child
    2. Find candidates where all prerequisites are mastered
    3. Score candidates by priority (difficulty, domain balance)
    4. Return top N candidates
    """
    # Step 1: Get mastered words
    mastered = await get_mastered_word_ids(child_id)

    # Step 2: Find candidates
    candidates = []
    for word in await get_all_enabled_words():
        if word.id in mastered:
            continue

        # Check prerequisites
        prerequisites = await get_prerequisites(word.id)
        if prerequisites.issubset(mastered):
            # Step 3: Calculate priority score
            score = calculate_priority(word, mastered)
            candidates.append((word, score))

    # Step 4: Sort and return top N
    candidates.sort(key=lambda x: x[1], reverse=True)
    return [word for word, _ in candidates[:limit]]


def calculate_priority(word: Word, mastered: Set[int]) -> float:
    """
    Calculate priority score for a word.

    Factors:
    - Difficulty: Prefer easier words first
    - Domain balance: Spread across domains
    - Prerequisite depth: Deeper words get slight boost
    """
    score = 100 - word.difficulty * 20  # Base score from difficulty

    # Domain balance (reduce if many words from same domain mastered)
    domain_mastered = count_by_domain(word.domain_id, mastered)
    score -= domain_mastered * 5

    # Prerequisite depth (slight boost for deeper words)
    depth = get_prerequisite_depth(word.id)
    score += depth * 2

    return score
```

### Graph Validation

```python
async def validate_graph(domain_id: int) -> bool:
    """
    Validate that the learning graph is a DAG.
    Returns True if valid, False otherwise.
    """
    words = await get_words_in_domain(domain_id)

    # Build adjacency list
    graph = {word.id: set() for word in words}
    async for word_id, prereq_id in get_prerequisites(domain_id):
        graph[word_id].add(prereq_id)

    # Detect cycles using DFS
    def has_cycle(node, visited={}, rec_stack={}):
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True

        rec_stack.remove(node)
        return False

    return not any(has_cycle(word.id) for word in words)
```

## API Communication Flow

### Authentication Flow

```
┌──────────┐                  ┌──────────┐                  ┌──────────┐
│ Client   │                  │ Backend  │                  │ Database │
└────┬─────┘                  └────┬─────┘                  └────┬─────┘
     │                             │                             │
     │ POST /api/v1/auth/login     │                             │
     │ {email, password}           │                             │
     ├────────────────────────────>│                             │
     │                             │ Verify password hash        │
     │                             ├────────────────────────────>│
     │                             │<────────────────────────────┤
     │                             │                             │
     │                             │ Generate JWT                │
     │<────────────────────────────┤                             │
     │ {access_token}              │                             │
     │                             │                             │
     │ GET /api/v1/domains         │                             │
     │ Authorization: Bearer <jwt> │                             │
     ├────────────────────────────>│                             │
     │                             │ Validate JWT                │
     │                             │ Return domains              │
     │<────────────────────────────┤                             │
```

### Learning Flow

```
┌──────────┐                  ┌──────────┐                  ┌──────────┐
│ Client   │                  │ Backend  │                  │ Database │
└────┬─────┘                  └────┬─────┘                  └────┬─────┘
     │                             │                             │
     │ GET /progress/child/{id}/next-words                       │
     ├────────────────────────────>│                             │
     │                             │ LearningService             │
     │                             │ - Get mastered words        │
     │                             │ - Find unlockable words     │
     │                             │ - Score & rank              │
     │                             ├────────────────────────────>│
     │                             │<────────────────────────────┤
     │<────────────────────────────┤                             │
     │ {words: [...]}               │                             │
     │                             │                             │
     │ POST /progress/child/{id}/word/{wid}/attempt              │
     │ {correct: true}              │                             │
     ├────────────────────────────>│                             │
     │                             │ ProgressService             │
     │                             │ - Update status             │
     │                             │ - Check for unlocks         │
     │                             ├────────────────────────────>│
     │                             │<────────────────────────────┤
     │                             │ Check if 3+ successful      │
     │                             │ -> mastered                │
     │<────────────────────────────┤                             │
     │ {status: "mastered", unlocked_words: [...]}               │
```

## Security Architecture

### Authentication
- **Password Hashing**: bcrypt with salt
- **JWT Tokens**: Short-lived access tokens (15 min) + refresh tokens
- **Token Storage**: HttpOnly cookies or secure localStorage

### Authorization
- **Parent-Child Link**: Parents can only access their own children
- **API Protection**: All routes (except auth) require valid JWT
- **CORS**: Configured for specific frontend domains

### Input Validation
- **Pydantic Schemas**: All inputs validated via Pydantic models
- **SQL Injection Protection**: SQLAlchemy parameterized queries
- **XSS Prevention**: React automatic escaping

## Performance Considerations

### Database Indexes
- `users.email` - Unique index for login lookups
- `progress(child_id, word_id)` - Composite index for progress queries
- `word_prerequisites(word_id, prerequisite_id)` - Graph traversal
- `words.domain_id, enabled` - Domain word listings

### Caching Strategy
- **Frontend**: Zustand stores with API response caching
- **Backend**: Consider Redis for session data (future)
- **Database**: Connection pooling via SQLAlchemy async

### Async Operations
All database operations use SQLAlchemy 2.0 async for non-blocking I/O.
