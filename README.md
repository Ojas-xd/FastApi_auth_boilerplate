# FastAPI Auth Boilerplate

A production-ready authentication boilerplate built with FastAPI, PostgreSQL, Redis, and Celery. Includes JWT-based auth, email verification, and background task processing.

## Features

- User registration with email verification
- JWT access & refresh tokens
- Background email sending via Celery + Redis
- PostgreSQL database with SQLAlchemy ORM
- Password hashing with bcrypt
- Token expiry & re-verification flow

## Project Structure

```
FastApi_auth_boilerplate/
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── auth.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   ├── user.py
│   │   └── verification.py
│   ├── schemas/
│   │   └── user.py
│   ├── services/
│   │   ├── auth_services.py
│   │   ├── celery_app.py
│   │   ├── mail.py
│   │   └── verification_service.py
│   ├── database.py
│   ├── dependencies.py
│   └── main.py
├── .env
├── .env.example
└── .gitignore
```

## Prerequisites

- Python 3.10+
- PostgreSQL
- Docker (for Redis)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ojas-xd/FastApi_auth_boilerplate.git
cd FastApi_auth_boilerplate
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Setup environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

### 4. Start Redis via Docker

```bash
docker run -d --name redis -p 6379:6379 redis:alpine
```

### 5. Create PostgreSQL database

```sql
CREATE DATABASE auth_db;
```

> Tables are created automatically when the FastAPI server starts.

## Running the App

Open **3 terminals** from the project root:

**Terminal 1 — FastAPI server:**
```bash
uvicorn app.main:app --reload
```

**Terminal 2 — Celery worker:**
```bash
python -m celery -A app.services.celery_app worker --loglevel=info --pool=solo
```

> `--pool=solo` is required on Windows.

**Terminal 3 — Redis (if not already running):**
```bash
docker start redis
```

## Environment Variables

Copy `.env.example` and fill in your values:

```dotenv
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/auth_db

# JWT
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Mail (Gmail SMTP)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_FROM=your-email@gmail.com

# Redis
REDIS_URL=redis://localhost:6379/0
```

> For Gmail, use an **App Password** — not your actual Gmail password.
> Generate one at: Google Account → Security → 2-Step Verification → App Passwords

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login & get tokens |
| GET | `/auth/verify?token=...` | Verify email |

## API Usage

### Register

```bash
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

### Login

```bash
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

Response:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### Verify Email

Click the link sent to your email or hit:

```
GET /auth/verify?token=your-token-here
```

## Tech Stack

- **FastAPI** — Web framework
- **PostgreSQL** — Database
- **SQLAlchemy** — ORM
- **Redis** — Message broker
- **Celery** — Background task queue
- **FastAPI-Mail** — Email sending
- **python-jose** — JWT tokens
- **bcrypt** — Password hashing

## Notes

- Email verification is required before login
- If verification token expires, a new one is sent automatically on next login attempt
- Celery worker must be running for emails to be sent
