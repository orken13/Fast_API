# FastAPI Project

A production-ready REST API built with FastAPI, PostgreSQL, Alembic, and JWT authentication.

---

## Stack

```
FastAPI     → web framework
PostgreSQL  → database (runs in Docker)
SQLAlchemy  → ORM (Python ↔ DB)
Alembic     → database migrations
JWT         → authentication
bcrypt      → password hashing
```

---

## Project Structure

```
Fast_API/
├── app/
│   ├── main.py        # API endpoints
│   ├── models.py      # SQLAlchemy models (DB tables)
│   ├── schemas.py     # Pydantic models (request/response)
│   ├── database.py    # DB connection + session
│   └── auth.py        # JWT token + password hashing
├── migrations/        # Alembic migration files
└── alembic.ini        # Alembic config
```

---

## Setup

### 1. Start PostgreSQL with Docker

```bash
docker run -d \
  --name postgres \
  -e POSTGRES_USER=emel \
  -e POSTGRES_PASSWORD=1234 \
  -e POSTGRES_DB=fastapi_db \
  -p 5432:5432 \
  postgres
```

If Docker container is stopped, restart it:
```bash
docker start postgres
```

### 2. Install dependencies

```bash
pip3 install fastapi uvicorn sqlalchemy psycopg2-binary alembic pyjwt passlib[bcrypt] --break-system-packages
```

### 3. Run database migrations

```bash
alembic upgrade head
```

### 4. Start the server

```bash
uvicorn app.main:app --reload
```

API docs available at: `http://127.0.0.1:8000/docs`

---

## API Endpoints

### Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Create a new account |
| POST | `/login` | Login and get JWT token |

### Users (protected — JWT required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | List all users |
| GET | `/users/{id}` | Get a single user |
| PUT | `/users/{id}` | Update a user |
| DELETE | `/users/{id}` | Delete a user |
| GET | `/profile` | Get current user |

---

## Usage

### Register
```bash
curl -X POST http://127.0.0.1:8000/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Emel", "email": "emel@example.com", "password": "1234"}'
```

### Login (get token)
```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{"name": "Emel", "email": "emel@example.com", "password": "1234"}'
```

### Access protected endpoint
```bash
curl http://127.0.0.1:8000/users \
  -H "Authorization: Bearer <your_token_here>"
```

### Without token (returns 401)
```bash
curl http://127.0.0.1:8000/users
# {"detail": "Not authenticated"}
```

---

## How JWT works

```
1. Register → password is hashed (bcrypt) → saved to DB
2. Login    → password verified → JWT token generated
3. Request  → token sent in Authorization header → verified → access granted
4. No token → 401 Unauthorized
```

---

## Database Migrations (Alembic)

```bash
# Create a new migration after model changes
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Roll back one step
alembic downgrade -1

# View migration history
alembic history
```