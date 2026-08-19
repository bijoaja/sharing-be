from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_db
from app.modules.posts.repository import PostRepository
from app.modules.posts.service import PostService

def get_post_repository(db: AsyncSession = Depends(get_db)) -> PostRepository:
    return PostRepository(db)

def get_post_service(repo: PostRepository = Depends(get_post_repository)) -> PostService:
    return PostService(repo)
