# LearningToy API Reference

This document provides complete API reference documentation for the LearningToy backend.

## Base URL

```
http://localhost:8000  (development)
https://api.learningtoy.com  (production)
```

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## API Versions

Current API version: `v1`

All endpoints are prefixed with `/api/v1/`

---

## Health Check

### GET /health

Check if the API is running.

**Response:**
```json
{
  "status": "healthy"
}
```

---

## Authentication

### POST /api/v1/auth/register

Register a new parent account.

**Request Body:**
```json
{
  "email": "parent@example.com",
  "password": "securepassword123"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | Valid email address |
| password | string | Yes | Password (min 8 characters) |

**Response (201 Created):**
```json
{
  "id": "uuid",
  "email": "parent@example.com",
  "role": "parent",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Error (400 Bad Request):**
```json
{
  "detail": "Email already registered"
}
```

---

### POST /api/v1/auth/login

Login and receive JWT access token.

**Request Body:**
```json
{
  "email": "parent@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error (401 Unauthorized):**
```json
{
  "detail": "Invalid email or password"
}
```

---

### GET /api/v1/auth/me

Get current authenticated user info.

**Authentication:** Required

**Response (200 OK):**
```json
{
  "id": "uuid",
  "email": "parent@example.com",
  "role": "parent",
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

### GET /api/v1/auth/children

List all children for the authenticated parent.

**Authentication:** Required

**Response (200 OK):**
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "name": "Alice",
    "birth_date": "2018-05-15",
    "preferred_language": "en",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

---

### POST /api/v1/auth/children

Add a child profile to the authenticated parent's account.

**Authentication:** Required

**Request Body:**
```json
{
  "name": "Alice",
  "birth_date": "2018-05-15",
  "preferred_language": "en"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Child's name |
| birth_date | date | No | Child's birth date (ISO 8601) |
| preferred_language | string | No | Preferred language code (en, pl, es) |

**Response (201 Created):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "Alice",
  "birth_date": "2018-05-15",
  "preferred_language": "en",
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

## Domains

### GET /api/v1/domains

List all domains (system + user's custom domains).

**Authentication:** Required

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| include_system | boolean | true | Include system domains |

**Response (200 OK):**
```json
[
  {
    "id": "uuid",
    "user_id": null,
    "name": "Animals",
    "description": "Learn animal names in different languages",
    "icon": "🐾",
    "color": "#10b981",
    "is_system": true,
    "word_count": 11,
    "created_at": "2024-01-01T00:00:00Z"
  },
  {
    "id": "uuid",
    "user_id": "uuid",
    "name": "My Custom Words",
    "description": "Custom vocabulary",
    "icon": "📚",
    "color": "#3b82f6",
    "is_system": false,
    "word_count": 5,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

---

### POST /api/v1/domains

Create a custom domain.

**Authentication:** Required

**Request Body:**
```json
{
  "name": "My Custom Words",
  "description": "Custom vocabulary for learning",
  "icon": "📚",
  "color": "#3b82f6"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Domain name |
| description | string | No | Domain description |
| icon | string | No | Emoji icon |
| color | string | No | Hex color code |

**Response (201 Created):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "My Custom Words",
  "description": "Custom vocabulary for learning",
  "icon": "📚",
  "color": "#3b82f6",
  "is_system": false,
  "word_count": 0,
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

### GET /api/v1/domains/{domain_id}

Get domain details.

**Authentication:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain_id | UUID | Yes | Domain ID |

**Response (200 OK):**
```json
{
  "id": "uuid",
  "user_id": null,
  "name": "Animals",
  "description": "Learn animal names in different languages",
  "icon": "🐾",
  "color": "#10b981",
  "is_system": true,
  "word_count": 11,
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Error (404 Not Found):**
```json
{
  "detail": "Domain not found"
}
```

---

### GET /api/v1/domains/{domain_id}/words

Get all words in a domain.

**Authentication:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain_id | UUID | Yes | Domain ID |

**Response (200 OK):**
```json
[
  {
    "id": "uuid",
    "domain_id": "uuid",
    "difficulty": "beginner",
    "image_url": "https://example.com/dog.jpg",
    "sort_order": 1,
    "translations": [
      {
        "id": "uuid",
        "language": "en",
        "text": "Dog",
        "phonetic": "dɔːɡ",
        "example_sentence": "The dog is playing."
      },
      {
        "id": "uuid",
        "language": "pl",
        "text": "Pies",
        "phonetic": "pʲɛs",
        "example_sentence": "Pies się bawi."
      },
      {
        "id": "uuid",
        "language": "es",
        "text": "Perro",
        "phonetic": "ˈpe.ro",
        "example_sentence": "El perro está jugando."
      }
    ],
    "prerequisite_ids": [],
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

---

### POST /api/v1/domains/{domain_id}/words

Create a new word in a domain.

**Authentication:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain_id | UUID | Yes | Domain ID |

**Request Body:**
```json
{
  "difficulty": "beginner",
  "image_url": "https://example.com/dog.jpg",
  "sort_order": 1,
  "translations": [
    {
      "language": "en",
      "text": "Dog",
      "phonetic": "dɔːɡ",
      "example_sentence": "The dog is playing."
    },
    {
      "language": "pl",
      "text": "Pies",
      "phonetic": "pʲɛs",
      "example_sentence": "Pies się bawi."
    }
  ],
  "prerequisite_ids": []
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| difficulty | string | Yes | beginner | intermediate | advanced |
| image_url | string | No | URL to word image |
| sort_order | integer | No | Display order |
| translations | array | Yes | At least one translation |
| prerequisite_ids | array | No | Word IDs that must be learned first |

**Response (201 Created):**
```json
{
  "id": "uuid",
  "domain_id": "uuid",
  "difficulty": "beginner",
  "image_url": "https://example.com/dog.jpg",
  "sort_order": 1,
  "translations": [...],
  "prerequisite_ids": [],
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

### GET /api/v1/domains/{domain_id}/graph

Get learning graph for a domain (nodes, edges, levels).

**Authentication:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain_id | UUID | Yes | Domain ID |

**Response (200 OK):**
```json
{
  "domain_id": "uuid",
  "domain_name": "Animals",
  "nodes": [
    {
      "id": "uuid",
      "domain_id": "uuid",
      "difficulty": "beginner",
      "image_url": "https://example.com/dog.jpg",
      "translations": {
        "en": "Dog",
        "pl": "Pies",
        "es": "Perro"
      },
      "sort_order": 1
    }
  ],
  "edges": [
    {
      "from": "uuid",
      "to": "uuid"
    }
  ],
  "levels": [
    ["word-id-1", "word-id-2"],
    ["word-id-3", "word-id-4"]
  ]
}
```

---

## Progress

### GET /api/v1/progress/child/{child_id}

Get all progress records for a child.

**Authentication:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| child_id | UUID | Yes | Child ID (must belong to authenticated user) |

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain_id | UUID | No | Filter by domain |

**Response (200 OK):**
```json
[
  {
    "id": "uuid",
    "word_id": "uuid",
    "status": "mastered",
    "attempts": 5,
    "correct_count": 4,
    "streak_count": 3,
    "accuracy": 0.8,
    "last_practiced_at": "2024-01-01T12:00:00Z",
    "mastered_at": "2024-01-01T12:00:00Z"
  }
]
```

**Status Values:**
- `locked` - Prerequisites not met
- `unlocked` - Ready to learn
- `in_progress` - Started learning
- `practicing` - Needs more practice
- `mastered` - Successfully learned

---

### GET /api/v1/progress/child/{child_id}/overview

Get overview statistics for a child.

**Authentication:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| child_id | UUID | Yes | Child ID |

**Response (200 OK):**
```json
{
  "total_words": 50,
  "mastered": 15,
  "practicing": 8,
  "in_progress": 12,
  "unlocked": 10,
  "locked": 5,
  "total_attempts": 245,
  "total_correct": 196,
  "accuracy": 0.8
}
```

---

### GET /api/v1/progress/child/{child_id}/next-words

Get recommended next words for a child to learn.

**Authentication:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| child_id | UUID | Yes | Child ID |

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain_id | UUID | Yes | Filter by domain |
| limit | integer | No | Max words to return (default: 5) |

**Response (200 OK):**
```json
{
  "words": [
    {
      "word_id": "uuid",
      "word_text": {
        "en": "Cat",
        "pl": "Kot",
        "es": "Gato"
      },
      "status": "unlocked",
      "difficulty": "beginner"
    }
  ]
}
```

---

### POST /api/v1/progress/child/{child_id}/word/{word_id}/attempt

Record a practice attempt for a word.

**Authentication:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| child_id | UUID | Yes | Child ID |
| word_id | UUID | Yes | Word ID |

**Request Body:**
```json
{
  "correct": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| correct | boolean | Yes | Whether the attempt was correct |

**Response (200 OK):**
```json
{
  "id": "uuid",
  "word_id": "uuid",
  "status": "mastered",
  "attempts": 5,
  "correct_count": 4,
  "streak_count": 3,
  "accuracy": 0.8,
  "last_practiced_at": "2024-01-01T12:00:00Z",
  "mastered_at": "2024-01-01T12:00:00Z"
}
```

**Status Transition Rules:**
- After 3+ attempts with 80%+ accuracy → `mastered`
- After 3+ attempts with 60%+ accuracy and streak ≥ 2 → `practicing`
- Otherwise → `in_progress`

---

## Chat

### POST /api/v1/chat/message

Send a chat message and get AI response.

**Authentication:** Required

**Request Body:**
```json
{
  "child_id": "uuid",
  "session_id": null,
  "domain_id": "uuid",
  "message": "Hello!"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| child_id | UUID | Yes | Child ID |
| session_id | UUID | No | Existing session ID (null for new) |
| domain_id | UUID | No | Current learning domain |
| message | string | Yes | User's message |

**Response (200 OK):**
```json
{
  "session_id": "uuid",
  "message": {
    "role": "assistant",
    "content": "Hello! Let's learn some words together!",
    "word_id": null,
    "timestamp": "2024-01-01T12:00:00Z"
  }
}
```

**Note:** The current implementation uses a mock AI service. Future versions will integrate real AI.

---

### GET /api/v1/chat/sessions/{session_id}/history

Get message history for a chat session.

**Authentication:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| session_id | UUID | Yes | Session ID |

**Response (200 OK):**
```json
{
  "session_id": "uuid",
  "child_id": "uuid",
  "messages": [
    {
      "id": "uuid",
      "role": "user",
      "content": "Hello!",
      "word_id": null,
      "timestamp": "2024-01-01T12:00:00Z"
    },
    {
      "id": "uuid",
      "role": "assistant",
      "content": "Hello! Let's learn some words together!",
      "word_id": null,
      "timestamp": "2024-01-01T12:00:01Z"
    }
  ]
}
```

---

## Error Responses

All endpoints may return the following error responses:

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Interactive Documentation

When running the backend locally, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive API documentation where you can test endpoints directly.
