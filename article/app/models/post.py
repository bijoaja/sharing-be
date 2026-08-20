from datetime import datetime
from sqlalchemy import String, Text, TIMESTAMP, func, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.config.database import Base
from app.core.enums import PostStatus

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[PostStatus] = mapped_column(Enum(PostStatus, native_enum=False), nullable=False, default=PostStatus.DRAFT)
    created_date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )
    updated_date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
