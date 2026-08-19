from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class PostStatus(str, Enum):
    PUBLISH = "Publish"
    DRAFT = "Draft"
    TRASH = "Trash"

class CreatePostRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    category: str = Field(min_length=1, max_length=100)
    status: PostStatus = PostStatus.DRAFT

class UpdatePostRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
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
