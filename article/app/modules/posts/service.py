from typing import List, Tuple
from app.core.exceptions import NotFoundException
from app.models.post import Post
from app.modules.posts.repository import PostRepository
from app.modules.posts.schemas import CreatePostRequest, UpdatePostRequest

class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def create_post(self, request: CreatePostRequest) -> Post:
        post = Post(
            title=request.title,
            content=request.content,
            category=request.category,
            status=request.status.value,
        )
        return await self.repo.create(post)

    async def get_post(self, post_id: int) -> Post:
        post = await self.repo.find_by_id(post_id)
        if not post:
            raise NotFoundException("Article not found")
        return post

    async def list_posts(self, limit: int, offset: int) -> Tuple[List[Post], int]:
        posts = await self.repo.list_all(offset=offset, limit=limit)
        total = await self.repo.count_all()
        return posts, total

    async def update_post(self, post_id: int, request: UpdatePostRequest) -> Post:
        post = await self.get_post(post_id)
        data = request.model_dump(exclude_unset=True)
        if "status" in data and data["status"] is not None:
            data["status"] = data["status"].value
        return await self.repo.update(post, data)

    async def delete_post(self, post_id: int) -> Post:
        post = await self.get_post(post_id)
        return await self.repo.soft_delete(post)
