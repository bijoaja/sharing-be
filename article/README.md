# Article Service

FastAPI + MySQL. CRUD artikel dengan service layer, migrasi skema via Alembic. Port default `8001`.

## Setup env

```bash
cp .env.example .env
```

| Var | Keterangan |
|---|---|
| `DATABASE_URL` | `mysql+aiomysql://user:pass@host:3306/article` — koneksi database |
| `MYSQL_ROOT_PASSWORD` | kredensial root, dipakai `alembic/env.py` sekali untuk `CREATE DATABASE`/`CREATE USER`/`GRANT` |
| `ARTICLE_PORT` | port listen, default `8001` |
| `APP_ENV`, `DEBUG` | mode aplikasi |

Butuh MySQL 8.0 jalan (lihat root `README.md` untuk setup `db` via Docker).

## Cara Menjalankan — Docker

Sama untuk Ubuntu & Windows (Docker Desktop/WSL2), dari root repo:

```bash
docker compose -f ../docker-compose.dev.yml up -d db article   # dev
docker compose -f ../docker-compose.dev.yml exec article alembic upgrade head

docker compose -f ../docker-compose.yml up -d db article       # prod
docker compose -f ../docker-compose.yml exec article alembic upgrade head
```

## Cara Menjalankan — Manual (venv)

DB paling gampang tetap via container: `docker compose -f ../docker-compose.dev.yml up -d db`.

### Ubuntu / Linux
```bash
cd article
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### Windows (PowerShell)
```powershell
cd article
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## Migrasi

- Jalankan: `uv run alembic upgrade head` (atau `docker compose exec article alembic upgrade head`)
- Buat migrasi baru: `uv run alembic revision --autogenerate -m "pesan"`
- Bootstrap DB/user dilakukan otomatis oleh `alembic/env.py` via `MYSQL_ROOT_PASSWORD`, jadi database tidak perlu dibuat manual sebelumnya.

## Verifikasi

- `http://localhost:8001/health` → `{"success": true, ...}`
- `http://localhost:8001/docs` — Swagger UI
