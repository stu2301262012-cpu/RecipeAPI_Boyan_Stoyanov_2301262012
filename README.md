# Recipe Catalog API

REST API for a recipe catalog built with **FastAPI**, **SQLAlchemy** (SQLite), **Pydantic** and **Alembic**.

Author: Boyan Stoyanov, faculty number 2301262012

## Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
```

## Run

```bash
uvicorn app.main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs
