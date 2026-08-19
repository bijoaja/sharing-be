from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from app.config.logger import setup_logging
from app.core.middleware import RequestLoggingMiddleware
from app.core.exceptions import register_exception_handlers
from app.core.responses import ApiResponse
from app.modules.posts.router import router as posts_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield

app = FastAPI(title="Article Service", lifespan=lifespan)

app.add_middleware(RequestLoggingMiddleware)
register_exception_handlers(app)

health_router = APIRouter(tags=["Health"])

@health_router.get("/health", response_model=ApiResponse[dict])
async def health_check() -> ApiResponse[dict]:
    return ApiResponse(data={"status": "ok"})

app.include_router(health_router)
app.include_router(posts_router)
