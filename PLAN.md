# LearningToy - Implementation Plan

## Project Overview
A multilingual language learning platform for children with:
- **Device Emulator**: Web-based simulation of ESP32 device (screen, speaker, microphone)
- **Backend API**: FastAPI with learning graph and progress tracking
- **Parent Dashboard**: React web interface for monitoring and customization

## Tech Stack
- **Backend**: Python FastAPI + PostgreSQL + SQLAlchemy
- **Frontend**: React + Vite + TypeScript + Tailwind CSS + shadcn/ui
- **Graph Vis**: ReactFlow for interactive learning graph
- **State**: Zustand
- **AI**: Mock text chat (voice planned for later)

## Languages
Polish, Spanish, English (multilingual from day one)

---

## Project Structure

```
LearningToy/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   │   ├── user.py
│   │   │   ├── domain.py
│   │   │   ├── word.py
│   │   │   └── progress.py
│   │   ├── schemas/                # Pydantic schemas
│   │   ├── api/                    # Route handlers
│   │   │   ├── auth.py
│   │   │   ├── domains.py
│   │   │   ├── words.py
│   │   │   ├── progress.py
│   │   │   └── chat.py
│   │   ├── services/               # Business logic
│   │   │   ├── learning_service.py # Core learning algorithms
│   │   │   ├── graph_service.py    # Graph traversal
│   │   │   └── chat_service.py     # Mock AI chat
│   │   └── db/seed.py              # Sample data
│   ├── alembic/                    # Migrations
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DeviceEmulator/     # Child device simulator
│   │   │   │   ├── DeviceFrame.tsx
│   │   │   │   ├── DeviceScreen.tsx
│   │   │   │   ├── WordCard.tsx
│   │   │   │   └── ChatInterface.tsx
│   │   │   └── ParentDashboard/    # Parent interface
│   │   │       ├── ProgressOverview.tsx
│   │   │       ├── DomainGraph.tsx # ReactFlow visualization
│   │   │       └── DomainEditor.tsx
│   │   ├── services/               # API clients
│   │   ├── stores/                 # Zustand state
│   │   └── types/
│   └── package.json
│
├── docker-compose.yml
└── README.md
```

---

## Database Schema (Key Tables)

| Table | Purpose |
|-------|---------|
| `users` | Parent accounts |
| `children` | Child profiles linked to parents |
| `domains` | Word categories (Animals, Food & Home) |
| `words` | Individual words with difficulty level |
| `word_translations` | Multilingual text (en/pl/es) |
| `word_prerequisites` | Learning graph edges (DAG) |
| `progress` | Child's learning progress per word |
| `chat_sessions` | AI tutoring sessions |

### Progress Status Values
- `locked` - Prerequisites not met
- `unlocked` - Ready to learn
- `in_progress` - Started learning
- `practicing` - Needs more practice
- `mastered` - Successfully learned

---

## API Endpoints

| Route | Purpose |
|-------|---------|
| `POST /api/v1/auth/register` | Register parent |
| `POST /api/v1/auth/login` | Login with JWT |
| `GET /api/v1/domains` | List all domains |
| `POST /api/v1/domains` | Create custom domain |
| `GET /api/v1/domains/{id}/graph` | Get learning graph |
| `GET /api/v1/progress/child/{id}` | Get child progress |
| `POST /api/v1/progress/attempt` | Record practice attempt |
| `GET /api/v1/progress/next-words` | Get recommended words |
| `POST /api/v1/chat` | Send chat message |

---

## Sample Data: Two Domains

### Domain 1: Animals
| Difficulty | Words (EN / PL / ES) |
|------------|---------------------|
| Beginner | Dog / Pies / Perro, Cat / Kot / Gato, Bird / Ptak / Pájaro, Fish / Ryba / Pez |
| Intermediate | Rabbit / Królik / Conejo, Squirrel / Wiewiórka / Ardilla, Horse / Koń / Caballo, Cow / Krowa / Vaca |
| Advanced | Hedgehog / Jeż / Erizo, Fox / Lis / Zorro, Owl / Sowa / Búho |

### Domain 2: Food & Home
| Difficulty | Words (EN / PL / ES) |
|------------|---------------------|
| Beginner | Apple / Jabłko / Manzana, Bread / Chleb / Pan, Milk / Mleko / Leche, Water / Woda / Agua, Chair / Krzesło / Silla, Table / Stół / Mesa |
| Intermediate | Breakfast / Śniadanie / Desayuno, Cheese / Ser / Queso, Kitchen / Kuchnia / Cocina, Bedroom / Sypialnia / Dormitorio |
| Advanced | Refrigerator / Lodówka / Refrigerador, Sandwich / Kanapka / Sándwich, Soup / Zupa / Sopa |

---

## Implementation Phases

### Phase 1: Foundation (Backend)
1. Set up FastAPI project structure
2. Configure PostgreSQL + Alembic migrations
3. Implement database models
4. Implement auth endpoints (JWT)
5. Seed database with sample domains

### Phase 2: Core Logic
1. Implement `GraphService` (DAG build, traverse, validate)
2. Implement `LearningService` (next words, unlock logic)
3. Implement `ProgressService` (record attempts, status)
4. Add domain/word CRUD endpoints

### Phase 3: Frontend Foundation
1. Set up Vite + React + TypeScript
2. Configure Tailwind + shadcn/ui
3. Set up Zustand stores
4. Implement API service layer
5. Create login/register pages

### Phase 4: Parent Dashboard
1. Implement `ProgressOverview` component
2. Implement `DomainGraph` with ReactFlow
3. Create custom node components (status-based)
4. Implement `DomainEditor` and `WordEditor`

### Phase 5: Device Emulator
1. Implement `DeviceFrame` (physical device look)
2. Implement `DeviceScreen` with mode routing
3. Implement `WordCard` component
4. Implement learning flow
5. Implement `ChatInterface` (text-based, mock AI)

### Phase 6: Integration & Polish
1. Integration testing
2. Error handling and loading states
3. Responsive design
4. Docker Compose setup
5. Documentation

---

## Critical Files to Create

**Backend:**
- `backend/app/main.py` - FastAPI app entry
- `backend/app/models/word.py` - Word model with relationships
- `backend/app/models/progress.py` - Progress tracking
- `backend/app/services/learning_service.py` - Learning algorithms
- `backend/app/services/graph_service.py` - Graph traversal
- `backend/app/db/seed.py` - Sample data

**Frontend:**
- `frontend/src/components/ParentDashboard/DomainGraph.tsx` - ReactFlow visualization
- `frontend/src/components/DeviceEmulator/DeviceScreen.tsx` - Child learning interface
- `frontend/src/stores/progressStore.ts` - Progress state management

---

## Learning Graph Algorithm

The learning graph is a **Directed Acyclic Graph (DAG)**:
- **Nodes**: Words (with difficulty metadata)
- **Edges**: Prerequisite relationships (A must be learned before B)

```python
# Key algorithm: Get next recommended words
def get_next_words(mastered: Set[str], limit: int) -> List[str]:
    candidates = []
    for word_id in all_words:
        if word_id in mastered: continue
        # Check if all prerequisites are mastered
        if prerequisites[word_id].issubset(mastered):
            score = calculate_priority(word_id)
            candidates.append((word_id, score))
    return sorted(candidates, key=score, reverse=True)[:limit]
```

---

## Docker Compose Setup

```yaml
services:
  postgres: PostgreSQL 15
  backend: FastAPI with auto-reload
  frontend: Vite dev server
```

Run with: `docker-compose up`
