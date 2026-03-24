# MacroMetrics - Agent Coding Guidelines

This file provides guidelines for AI agents working on the MacroMetrics fitness SaaS project.

---

## Project Overview

- **Type**: Full-stack fitness SaaS (React + FastAPI + PostgreSQL)
- **Frontend**: React 19, Vite 8, Tailwind CSS 4, Framer Motion
- **Backend**: FastAPI, SQLAlchemy 2.0, Pydantic 2.x, Alembic
- **Database**: PostgreSQL with Alembic migrations

---

## Build Commands

### Backend

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload

# Run tests
pytest tests/ -v                    # All tests
pytest tests/test_auth.py -v        # Single test file
pytest tests/test_auth.py::TestRegisterRequest::test_valid_registration -v  # Single test

# Run migrations
alembic upgrade head               # Apply all migrations
alembic revision --autogenerate -m "description"  # Create new migration
alembic history                   # View migration history
alembic current                  # Check current migration
```

### Frontend

```bash
cd frontend
npm install
npm run dev        # Development server
npm run build      # Production build
npm run lint       # Lint code
```

---

## Code Style Guidelines

### Python (Backend)

#### Imports
- Standard library first, then third-party, then local
- Use absolute imports: `from database import get_db`
- Group: `from X import Y, Z`

```python
# Correct order
import os
import logging
from datetime import datetime, date

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field

from database import get_db
from models import User
from auth import require_auth
```

#### Naming Conventions
- **Functions**: `snake_case` (e.g., `get_user_by_email`)
- **Classes**: `PascalCase` (e.g., `UserProfile`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_LOGIN_ATTEMPTS`)
- **Private methods**: prefix with `_` (e.g., `_internal_helper`)

#### Type Hints
- Always use type hints for function parameters and return types
- Use `Optional[X]` instead of `X | None` for compatibility

```python
def get_user(user_id: int, db: Session = Depends(get_db)) -> Optional[User]:
    ...
```

#### Pydantic Models
- Use `Field` for validation with constraints
- Use `EmailStr` for email validation
- Use `Literal` for enum-like strings

```python
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    role: Literal["user", "admin"] = "user"
```

#### Error Handling
- Use HTTPException for API errors with appropriate status codes
- Log errors before raising

```python
from fastapi import HTTPException, status

if not user:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )
```

#### Database
- Use dependency injection: `db: Session = Depends(get_db)`
- Always close sessions or use `yield`
- Use SQLAlchemy relationships, not raw joins

---

### JavaScript/React (Frontend)

#### File Organization
- Pages in `src/pages/`
- Components in `src/components/`
- Contexts in `src/contexts/`
- API client in `src/api.js`

#### Naming
- Components: `PascalCase` (e.g., `UserProfile.jsx`)
- Hooks: `camelCase` starting with `use` (e.g., `useAuth`)
- Utils: `camelCase` (e.g., `formatDate.js`)

#### React Patterns
- Use functional components with hooks
- Destructure props properly
- Use Framer Motion for animations

```jsx
import { motion } from 'framer-motion';

function Card({ title, children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card"
    >
      {children}
    </motion.div>
  );
}
```

---

## Database Guidelines

### Alembic Migrations

1. Always use Alembic, never `Base.metadata.create_all()`
2. Generate migrations after model changes:
   ```bash
   alembic revision --autogenerate -m "add new table"
   ```
3. Test migrations locally before committing
4. Never modify existing migration files

### Models

- Always define relationships using `relationship()`
- Use indexes on frequently queried columns
- Use `cascade="all, delete-orphan"` for dependent relationships

---

## API Design

### REST Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/resource` | List all |
| GET | `/resource/{id}` | Get single |
| POST | `/resource` | Create new |
| PUT/PATCH | `/resource/{id}` | Update |
| DELETE | `/resource/{id}` | Delete |

### Response Format

```python
# Success
return {"message": "User created", "id": user.id}

# List
return {"items": [...], "total": count}

# Error
raise HTTPException(status_code=400, detail="Error message")
```

---

## Security Guidelines

1. Never commit secrets - use `.env` files
2. Always validate input with Pydantic
3. Use parameterized queries (SQLAlchemy handles this)
4. Rate limit sensitive endpoints
5. Hash passwords with bcrypt (already configured with rounds=12)

---

## Testing

### Python Tests

- Test files in `backend/tests/`
- Use `pytest` framework
- Test Pydantic validation separately from DB operations

```python
import pytest
from pydantic import ValidationError

def test_email_validation():
    with pytest.raises(ValidationError):
        UserCreate(email="invalid-email")
```

---

## Common Issues

### FastAPI + SlowAPI Rate Limiting
When using `@limiter.limit()`, always include `request: Request` as first parameter:

```python
@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, payload: LoginRequest, db: Session = Depends(get_db)):
    ...
```

### SQLAlchemy Column Issues
Don't use Python `bool` in conditional expressions - use SQLAlchemy columns directly:

```python
# Wrong
if user.is_active == True:

# Correct
if user.is_active:
```

---

## Project-Specific Notes

- JWT secret required in environment (no fallback)
- Database URL required (no fallback)
- Use `python -m data.seed_*` for seeding databases
- Alembic configured to read DATABASE_URL from `.env`
