# LearningToy

A multilingual language learning platform for children featuring a web-based device emulator, progressive learning graphs, and a parent dashboard.

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![React](https://img.shields.io/badge/react-18-blue)

## Screenshots

### Login Page
![Login Page](docs/screenshots/login-page.png)

### Parent Dashboard
![Parent Dashboard](docs/screenshots/dashboard.png)

### Device Emulator
![Device Emulator](docs/screenshots/device-emulator.png)

## Features

- **Device Emulator**: Web-based simulation of a physical learning device with screen and text chat
- **Learning Graph**: Progressive word learning using Directed Acyclic Graphs (DAG) from simple to advanced concepts
- **Parent Dashboard**: Track progress, view interactive domain graphs, and manage vocabulary
- **Multilingual**: Built-in support for English, Polish, and Spanish from day one
- **JWT Authentication**: Secure parent accounts with child profile management

## Tech Stack

### Backend
- **FastAPI** (Python 3.11+) - Modern, fast web framework
- **PostgreSQL 15** - Reliable relational database
- **SQLAlchemy 2.0 (async)** - Async ORM for database operations
- **Alembic** - Database migration tool
- **JWT** - Token-based authentication

### Frontend
- **React 18 + Vite** - Fast build tool and dev server
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Zustand** - Lightweight state management
- **React Router** - Client-side routing
- **ReactFlow** - Interactive graph visualization

## Documentation

- **[Architecture Guide](docs/architecture.md)** - System design, database schema, and learning algorithms
- **[API Reference](docs/api.md)** - Complete API endpoint documentation with examples
- **[Deployment Guide](docs/deployment.md)** - Production deployment instructions for various platforms
- **[Implementation Plan](PLAN.md)** - Detailed development roadmap

---

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# Seed the database with sample data
docker-compose exec backend python run_seed.py
```

Then visit:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development

**Backend:**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Start PostgreSQL (using Docker)
docker run -d --name learningtoy-db \
  -e POSTGRES_USER=learningtoy \
  -e POSTGRES_PASSWORD=learningtoy \
  -e POSTGRES_DB=learningtoy \
  -p 5432:5432 \
  postgres:15-alpine

# Seed the database
python run_seed.py

# Run the server
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

## Sample Data

The seed script creates two domains with learning graphs:

### Animals Domain
- **Beginner**: Dog, Cat, Bird, Fish
- **Intermediate**: Rabbit, Squirrel, Horse, Cow
- **Advanced**: Hedgehog, Fox, Owl

### Food & Home Domain
- **Beginner**: Apple, Bread, Milk, Water, Chair, Table
- **Intermediate**: Breakfast, Cheese, Kitchen
- **Advanced**: Refrigerator, Sandwich, Soup

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new parent account
- `POST /api/v1/auth/login` - Login and receive JWT
- `GET /api/v1/auth/me` - Get current user info
- `GET /api/v1/auth/children` - List parent's children
- `POST /api/v1/auth/children` - Add child profile

### Domains
- `GET /api/v1/domains` - List all domains
- `GET /api/v1/domains/{id}` - Get domain details
- `GET /api/v1/domains/{id}/words` - Get all words in domain
- `GET /api/v1/domains/{id}/graph` - Get learning graph

### Progress
- `GET /api/v1/progress/child/{id}/overview` - Dashboard statistics
- `GET /api/v1/progress/child/{id}/next-words` - Get recommended words
- `POST /api/v1/progress/child/{id}/word/{word_id}/attempt` - Record practice attempt

### Chat
- `POST /api/v1/chat/message` - Send chat message, get AI response (mock)

## Project Structure

```
LearningToy/
├── backend/
│   ├── app/
│   │   ├── api/              # API route handlers
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   └── db/seed.py        # Sample data
│   ├── alembic/              # Database migrations
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DeviceEmulator/   # Child device simulator
│   │   │   └── ParentDashboard/  # Parent interface
│   │   ├── services/         # API clients
│   │   ├── stores/           # Zustand state
│   │   └── pages/            # Page components
│   └── package.json
│
└── docker-compose.yml
```

## Development Roadmap

- [ ] Voice chat integration (OpenAI/Anthropic)
- [ ] ESP32 hardware device support
- [ ] More domains and vocabulary
- [ ] Gamification (streaks, badges)
- [ ] Sibling leaderboard
- [ ] Offline mode with service workers

---

## Learning Progress States

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

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
