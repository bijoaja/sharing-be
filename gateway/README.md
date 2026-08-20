# Gateway Service

FastAPI reverse proxy. Meneruskan semua request `/article*` ke [article service](../article/README.md) via `ARTICLE_SERVICE_URL`. Port default `8000`.

## Setup env

```bash
cp .env.example .env
```

| Var | Keterangan |
|---|---|
| `GATEWAY_PORT` | port listen, default `8000` |
| `ARTICLE_SERVICE_URL` | base URL service article, contoh `http://article:8001` (Internal Docker) / `http://localhost:8001` (Eksternal) |
| `APP_ENV`, `DEBUG` | mode aplikasi |

## Cara Menjalankan — Docker

Sama untuk Ubuntu & Windows (Docker Desktop/WSL2), dari root repo:

```bash
docker compose -f ../docker-compose.dev.yml up -d gateway   # dev
docker compose -f ../docker-compose.yml up -d gateway       # prod
```

## Cara Menjalankan — Manual (venv)

Butuh article service sudah jalan (lihat `article/README.md`) supaya proxy ada target.

### Ubuntu / Linux
```bash
cd gateway
uv sync
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Windows (PowerShell)
```powershell
cd gateway
uv sync
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Verifikasi

- `http://localhost:8000/health` → `{"success": true, ...}`
- `http://localhost:8000/docs` — Swagger UI
- `http://localhost:8000/article/...` — diteruskan ke article service
