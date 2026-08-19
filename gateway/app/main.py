import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, APIRouter, Request, Response

from app.config.logger import setup_logging
from app.config.settings import settings

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield

app = FastAPI(title="Gateway Service", lifespan=lifespan)

health_router = APIRouter(tags=["Health"])

@health_router.get("/health")
async def health_check() -> dict:
    return {"success": True, "message": "Success", "data": {"status": "ok"}}

app.include_router(health_router)

HOP_BY_HOP_HEADERS = {"host", "content-length", "connection", "transfer-encoding"}

@app.api_route(
    "/article{path:path}",
    methods=["GET", "POST", "PATCH", "DELETE"],
)
async def proxy_article(path: str, request: Request) -> Response:
    forward_headers = {
        k: v for k, v in request.headers.items() if k.lower() not in HOP_BY_HOP_HEADERS
    }
    body = await request.body()

    async with httpx.AsyncClient(base_url=settings.ARTICLE_SERVICE_URL, timeout=30.0) as client:
        upstream = await client.request(
            method=request.method,
            url=f"/article{path}",
            headers=forward_headers,
            content=body,
            params=request.query_params,
        )

    response_headers = {
        k: v for k, v in upstream.headers.items() if k.lower() not in HOP_BY_HOP_HEADERS
    }
    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        headers=response_headers,
        media_type=upstream.headers.get("content-type"),
    )
