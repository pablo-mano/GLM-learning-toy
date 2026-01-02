# LearningToy Documentation

Welcome to the LearningToy documentation. LearningToy is a multilingual language learning platform for children featuring a web-based device emulator, progressive learning graphs, and a parent dashboard.

## Quick Links

- [Getting Started](#getting-started)
- [Architecture](architecture.md)
- [API Reference](api.md)
- [Deployment](deployment.md)

## Getting Started

### What is LearningToy?

LearningToy is an educational platform that helps children learn new languages through:

- **Device Emulator**: A web-based simulation of a physical learning device with an interactive screen and chat interface
- **Learning Graph**: A progressive learning system using Directed Acyclic Graphs (DAG) to structure vocabulary from simple to advanced
- **Parent Dashboard**: A web interface for parents to track progress, visualize learning paths, and manage vocabulary domains
- **Multilingual Support**: Built-in support for English, Polish, and Spanish

### Quick Start with Docker

The fastest way to get started is using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/yourusername/LearningToy.git
cd LearningToy

# Start all services (backend, frontend, database)
docker-compose up -d

# Seed the database with sample learning domains
docker-compose exec backend python run_seed.py
```

Then visit:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs

### Project Structure

```
LearningToy/
├── backend/                 # FastAPI Python backend
│   ├── app/
│   │   ├── api/            # API route handlers
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── schemas/        # Pydantic validation schemas
│   │   ├── services/       # Business logic layer
│   │   └── db/seed.py      # Sample data generator
│   ├── alembic/            # Database migrations
│   └── requirements.txt
│
├── frontend/                # React TypeScript frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── DeviceEmulator/    # Child device interface
│   │   │   └── ParentDashboard/   # Parent admin interface
│   │   ├── services/       # API client layer
│   │   ├── stores/         # Zustand state management
│   │   └── types/          # TypeScript definitions
│   └── package.json
│
└── docker-compose.yml       # Development environment
```

## Technology Stack

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI (Python 3.11+), PostgreSQL 15, SQLAlchemy 2.0 async |
| **Frontend** | React 18, Vite, TypeScript, Tailwind CSS, Zustand |
| **Visualization** | ReactFlow for learning graph display |
| **Authentication** | JWT tokens |
| **Containerization** | Docker, Docker Compose |

## Sample Learning Domains

The platform includes two pre-configured domains:

### Animals Domain
| Level | Words |
|-------|-------|
| Beginner | Dog, Cat, Bird, Fish |
| Intermediate | Rabbit, Squirrel, Horse, Cow |
| Advanced | Hedgehog, Fox, Owl |

### Food & Home Domain
| Level | Words |
|-------|-------|
| Beginner | Apple, Bread, Milk, Water, Chair, Table |
| Intermediate | Breakfast, Cheese, Kitchen, Bedroom |
| Advanced | Refrigerator, Sandwich, Soup |

Each word includes translations in English, Polish, and Spanish with phonetic guides.

## Documentation

- **[Architecture Guide](architecture.md)** - System design, database schema, and learning algorithms
- **[API Reference](api.md)** - Complete API endpoint documentation
- **[Deployment Guide](deployment.md)** - Production deployment instructions

## License

[Your License Here]
