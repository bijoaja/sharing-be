from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.core.enums import PostStatus

class CreatePostRequest(BaseModel):
    title: str = Field(min_length=20, max_length=255)
    content: str = Field(min_length=200)
    category: str = Field(min_length=3, max_length=100)
    status: PostStatus = PostStatus.DRAFT

class UpdatePostRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=20, max_length=255)
    content: Optional[str] = Field(None, min_length=200)
    category: Optional[str] = Field(None, min_length=3, max_length=100)
    status: Optional[PostStatus] = None

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    status: PostStatus
    created_date: datetime
    updated_date: datetime

    model_config = ConfigDict(from_attributes=True)
