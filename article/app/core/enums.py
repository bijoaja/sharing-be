from enum import Enum


class PostStatus(str, Enum):
    """Status artikel: publish (published), draft (unpublished), thrash (deleted)."""
    PUBLISH = "publish"
    DRAFT = "draft"
    THRASH = "thrash"
