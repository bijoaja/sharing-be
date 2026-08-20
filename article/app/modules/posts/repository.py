from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post import Post

class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, post: Post) -> Post:
        self.db.add(post)
        await self.db.flush()
        await self.db.refresh(post)
        return post

    async def find_by_id(self, post_id: int) -> Optional[Post]:
        stmt = select(Post).where(Post.id == post_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self, offset: int, limit: int) -> List[Post]:
        stmt = select(Post).order_by(Post.id.desc()).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_all(self) -> int:
        stmt = select(func.count(Post.id))
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def update(self, post: Post, data: dict) -> Post:
        for key, value in data.items():
            setattr(post, key, value)
        await self.db.flush()
        await self.db.refresh(post)
        return post

    async def soft_delete(self, post: Post) -> Post:
        post.status = "thrash"
        await self.db.flush()
        await self.db.refresh(post)
        return post
