from fastapi import APIRouter, Depends, Path
from app.core.dependencies import get_post_service
from app.core.responses import ApiResponse, ApiListResponse
from app.core.pagination import build_pagination_info
from app.modules.posts.schemas import CreatePostRequest, UpdatePostRequest, PostResponse
from app.modules.posts.service import PostService

router = APIRouter(prefix="/article", tags=["Article"])

@router.post("", response_model=ApiResponse[PostResponse], status_code=201)
async def create_article(
    request: CreatePostRequest,
    service: PostService = Depends(get_post_service),
) -> ApiResponse[PostResponse]:
    post = await service.create_post(request)
    return ApiResponse(data=PostResponse.model_validate(post))

@router.get("/{limit}/{offset}", response_model=ApiListResponse[PostResponse])
async def list_articles(
    limit: int = Path(ge=1, le=100),
    offset: int = Path(ge=0),
    service: PostService = Depends(get_post_service),
) -> ApiListResponse[PostResponse]:
    posts, total = await service.list_posts(limit=limit, offset=offset)
    response_data = [PostResponse.model_validate(p) for p in posts]
    page = (offset // limit) + 1 if limit > 0 else 1
    pagination = build_pagination_info(page=page, per_page=limit, total=total)
    return ApiListResponse(data=response_data, pagination=pagination)

@router.get("/{id}", response_model=ApiResponse[PostResponse])
async def get_article(
    id: int,
    service: PostService = Depends(get_post_service),
) -> ApiResponse[PostResponse]:
    post = await service.get_post(id)
    return ApiResponse(data=PostResponse.model_validate(post))

@router.patch("/{id}", response_model=ApiResponse[PostResponse])
async def update_article(
    id: int,
    request: UpdatePostRequest,
    service: PostService = Depends(get_post_service),
) -> ApiResponse[PostResponse]:
    post = await service.update_post(id, request)
    return ApiResponse(data=PostResponse.model_validate(post))

@router.delete("/{id}", response_model=ApiResponse[dict])
async def delete_article(
    id: int,
    service: PostService = Depends(get_post_service),
) -> ApiResponse[dict]:
    await service.delete_post(id)
    return ApiResponse(data={"message": "Article moved to trash"})
