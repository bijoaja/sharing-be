# Sharing BE

Backend microservices: **gateway** (FastAPI reverse proxy, port `8000`) meneruskan request `/article*` ke **article** (FastAPI port `8001`)..

```
be/
├── gateway/   # reverse proxy
├── article/   # CRUD artikel
├── docker-compose.yml       # prod
├── docker-compose.dev.yml   # dev
└── Makefile                 # shortcut docker compose
```

## Prasyarat

- Docker + Docker Compose (cara Docker)
- Python 3.12+ dan [uv](https://docs.astral.sh/uv/) (cara manual/venv)
- MySQL 8.0 jalan lokal jika tidak pakai Docker untuk `db`

## 1. Setup env

Salin tiap `.env.example` jadi `.env` (root, `gateway/`, `article/`) sesuaikan config environtment:

```bash
cp .env.example .env
cp gateway/.env.example gateway/.env
cp article/.env.example article/.env
```

| File | Var penting |
|---|---|
| `.env` (root) | `MYSQL_ROOT_PASSWORD`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE` — kredensial container `db` |
| `article/.env` | `DATABASE_URL` (`mysql+aiomysql://user:pass@host:3306/article`), `MYSQL_ROOT_PASSWORD` (dipakai alembic bootstrap), `ARTICLE_PORT` |
| `gateway/.env` | `ARTICLE_SERVICE_URL` (URL ke service article), `GATEWAY_PORT` |

## 2. Cara Menjalankan — Docker (Recommended)

Sama untuk Ubuntu dan Windows (via Docker Desktop/WSL2), jalankan dari root repo.

**Dev:**
```bash
docker compose -f docker-compose.dev.yml up -d
docker compose -f docker-compose.dev.yml exec article alembic upgrade head
```

**Prod:**
```bash
docker compose up -d
docker compose exec article alembic upgrade head
```

Atau pakai `Makefile` (butuh `make`; di Windows jalankan dari WSL/Git Bash):
```bash
make up-dev      # / make up     untuk prod
make migrate-dev # / make migrate
```

Cek service jalan: `curl http://localhost:8000/health` (gateway), `curl http://localhost:8001/health` (article).

Stop: `docker compose -f docker-compose.dev.yml down` (tambah `-v` untuk hapus volume MySQL).

## 3. Cara Menjalankan — Manual (venv)

DB tetap butuh MySQL — paling gampang tetap pakai container `db` saja: `docker compose -f docker-compose.dev.yml up -d db`. Lalu jalankan gateway & article langsung di host.

### Ubuntu / Linux

```bash
# install uv sekali saja
curl -LsSf https://astral.sh/uv/install.sh | sh

# article
cd article
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# gateway (terminal terpisah)
cd gateway
uv sync
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Windows (PowerShell)

```powershell
# article
cd article
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# gateway (terminal terpisah)
cd gateway
uv sync
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

`uv sync` otomatis bikin `.venv` dan install dependency dari `pyproject.toml` — tidak perlu `python -m venv` / `activate` manual selama pakai `uv run`. Kalau mau aktivasi manual: `.venv/bin/activate` (Ubuntu) atau `.venv\Scripts\Activate.ps1` (Windows).

## Referensi cepat

| Service | Port dev/prod | Docs |
|---|---|---|
| gateway | 8000 | `http://localhost:8000/docs` |
| article | 8001 | `http://localhost:8001/docs` |
| db (MySQL) | 3306 | — |
