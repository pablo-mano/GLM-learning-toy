# Deployment Guide

This guide covers deploying LearningToy to production environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Database Setup](#database-setup)
- [SSL/TLS Configuration](#ssltls-configuration)
- [Monitoring](#monitoring)

---

## Prerequisites

### Required Software
- Docker 20.10+ and Docker Compose 2.0+
- PostgreSQL 15 (or managed database service)
- Domain name (for production)
- SSL certificate (for HTTPS)

### Required Services
- PostgreSQL database
- Reverse proxy (Nginx/Caddy) recommended
- Container registry (Docker Hub, GHCR, etc.)

---

## Environment Variables

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/learningtoy

# JWT Settings
SECRET_KEY=your-super-secret-key-change-this
ACCESS_TOKEN_EXPIRE_MINUTES=15
ALGORITHM=HS256

# CORS
FRONTEND_URL=https://your-domain.com

# Environment
ENVIRONMENT=production
DEBUG=false
```

### Frontend Environment Variables

Create a `.env` file in the `frontend/` directory:

```bash
VITE_API_URL=https://api.your-domain.com
VITE_APP_TITLE=LearningToy
```

### Production `.env` Example

```bash
# backend/.env.production
DATABASE_URL=postgresql+asyncpg://learningtoy:secure-password@db.example.com:5432/learningtoy
SECRET_KEY=generated-secure-random-key-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=15
ALGORITHM=HS256
FRONTEND_URL=https://learningtoy.com
ENVIRONMENT=production
DEBUG=false
```

**Important:** Never commit `.env` files to version control.

---

## Docker Deployment

### Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    restart: always
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    restart: always
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@postgres:5432/${DB_NAME}
      SECRET_KEY: ${SECRET_KEY}
      FRONTEND_URL: ${FRONTEND_URL}
    networks:
      - internal
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        VITE_API_URL: ${VITE_API_URL}
    restart: always
    depends_on:
      - backend
    networks:
      - internal
    ports:
      - "80:80"

volumes:
  postgres_data:

networks:
  internal:
```

### Deploy with Docker Compose

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d

# Run database migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Seed database (optional)
docker-compose -f docker-compose.prod.yml exec backend python run_seed.py

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

---

## Cloud Deployment

### Railway

1. Connect your GitHub repository to Railway
2. Create two services: `learningtoy-backend` and `learningtoy-frontend`
3. Add a PostgreSQL service
4. Configure environment variables for each service
5. Deploy!

### Render

**Backend Deployment:**

1. Create a new Web Service
2. Connect your GitHub repository
3. Set root directory to `backend`
4. Configure build command:
   ```bash
   pip install -r requirements.txt
   ```
5. Configure start command:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
6. Add environment variables

**Frontend Deployment:**

1. Create a new Static Site
2. Connect your GitHub repository
3. Set root directory to `frontend`
4. Configure build command:
   ```bash
   npm run build
   ```
5. Set publish directory to `dist`
6. Add environment variables including `VITE_API_URL`

### AWS ECS

```yaml
# task-definition.json
{
  "family": "learningtoy",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "your-registry/learningtoy-backend:latest",
      "portMappings": [{"containerPort": 8000}],
      "environment": [
        {"name": "DATABASE_URL", "value": "..."},
        {"name": "SECRET_KEY", "value": "..."}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/learningtoy",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "backend"
        }
      }
    }
  ]
}
```

### DigitalOcean App Platform

1. Create a new app
2. Add your GitHub repository
3. Create components:
   - **Backend**: Python component, root `backend/`
   - **Frontend**: Static site component, root `frontend/`
   - **Database**: PostgreSQL addon
4. Configure environment variables
5. Deploy!

---

## Database Setup

### Running Migrations

```bash
# Generate new migration
alembic revision --autogenerate -m "description"

# Apply all migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

### Database Backup

```bash
# Backup
pg_dump -U user -h host learningtoy > backup.sql

# Restore
psql -U user -h host learningtoy < backup.sql
```

### Managed Database Backups

For production, use your cloud provider's automated backup system:
- AWS RDS: Automated backups and snapshots
- Google Cloud SQL: Automated backups
- Railway: Built-in backups
- Render: Automated backups

---

## SSL/TLS Configuration

### Using Caddy (Recommended)

Caddy automatically handles HTTPS with Let's Encrypt:

```dockerfile
# Caddyfile
learningtoy.com {
    reverse_proxy frontend:80
}

api.learningtoy.com {
    reverse_proxy backend:8000
}
```

Add to `docker-compose.yml`:

```yaml
caddy:
  image: caddy:2
  restart: always
  ports:
    - "80:80"
    - "443:443"
    - "443:443/udp"  # HTTP/3
  volumes:
    - ./Caddyfile:/etc/caddy/Caddyfile
    - caddy_data:/data
    - caddy_config:/config
```

### Using Nginx

```nginx
# /etc/nginx/sites-available/learningtoy
server {
    listen 80;
    server_name learningtoy.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name learningtoy.com;

    ssl_certificate /etc/letsencrypt/live/learningtoy.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/learningtoy.com/privkey.pem;

    location / {
        proxy_pass http://frontend:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 443 ssl http2;
    server_name api.learningtoy.com;

    ssl_certificate /etc/letsencrypt/live/api.learningtoy.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.learningtoy.com/privkey.pem;

    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Monitoring

### Health Checks

Backend provides health check endpoints:

- `GET /health` - Basic health check
- `GET /` - API info

Configure your load balancer or orchestrator to use these.

### Logging

**Backend Logging (Python):**

```python
# app/core/logging.py
import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO if settings.ENVIRONMENT == "production" else logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
```

**Structured Logging (JSON):**

For production, use structured logging:

```bash
pip install python-json-logger
```

```python
from pythonjsonlogger import jsonlogger

handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
```

### Metrics

Consider adding:
- Prometheus metrics (`prometheus-fastapi-instrumentator`)
- Error tracking (Sentry)
- Uptime monitoring (UptimeRobot, Pingdom)

### Performance Monitoring

```bash
# Install APM agent
pip install opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-fastapi
```

---

## Security Checklist

- [ ] Change all default passwords
- [ ] Use strong `SECRET_KEY` (min 32 chars, randomly generated)
- [ ] Enable HTTPS/TLS
- [ ] Set `DEBUG=false` in production
- [ ] Configure proper CORS origins
- [ ] Enable database backups
- [ ] Set up firewall rules
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting
- [ ] Set up log aggregation

---

## Troubleshooting

### Common Issues

**1. Database Connection Errors**

```bash
# Check database is reachable
docker-compose exec backend python -c "from app.database import engine; print('OK')"
```

**2. Frontend API Connection**

Ensure `VITE_API_URL` is set correctly in production.

**3. JWT Token Issues**

Check `SECRET_KEY` is consistent across deployments.

**4. CORS Errors**

Verify `FRONTEND_URL` matches your actual frontend domain.

### Debug Mode

Enable debug mode temporarily:

```bash
DEBUG=true docker-compose up backend
```

---

## Scaling Considerations

### Horizontal Scaling

- Run multiple backend instances behind a load balancer
- Use external session storage (Redis) for JWT refresh tokens
- Use managed PostgreSQL with read replicas

### Caching

Consider adding Redis for:
- Session storage
- API response caching
- Rate limiting

### CDN

Serve static assets via CDN:
- Frontend build artifacts
- Word images
- Static content
