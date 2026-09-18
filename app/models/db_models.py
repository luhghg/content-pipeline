from app.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func, ForeignKey, Text, BigInteger
from enum import Enum
from datetime import datetime
from typing import List, Optional

class ContentType(Enum):
    ARTICLE = "article"
    TWEET = "tweet"


class Status(Enum):
    QUEUED = "queued"          # создан, ждёт генерации
    GENERATING = "generating"      # идёт вызов LLM
    CHECKING = "checking"        # идёт проверка качества
    NEEDS_REVIEW = "needs_review"    # ждёт человека — здесь процесс спит
    APPROVED = "approved"        # прошло (автоматом или человеком)
    REJECTED = "rejected"        # человек отклонил
    FAILED = "failed"          # техническая ошибка, ретраи исчерпаны


class ApprovalType(Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"



class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[ContentType] = mapped_column(nullable=False)
    prompt_hint: Mapped[Optional[str]] = mapped_column(default=None, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true", nullable=False)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(default=None, nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)

    topic_contents: Mapped[List["ContentItem"]] = relationship(back_populates="topic")


class Reviewer(Base):
    __tablename__ = "reviewers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true", nullable=False)

    approved_contents: Mapped[List["ContentItem"]] = relationship(back_populates="approved_by")



class ContentItem(Base):
    __tablename__ = "content_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id", ondelete="RESTRICT"), nullable=False )
    content_type: Mapped[ContentType] = mapped_column(nullable=False)
    status: Mapped[Status] = mapped_column(nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=True)
    scheduled_for: Mapped[Optional[datetime]] = mapped_column(nullable=True, index=True)
    approval_type: Mapped[Optional[ApprovalType]] = mapped_column(default=None, nullable=True)

    approved_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("reviewers.id", ondelete="RESTRICT"), nullable=True)
    approved_by: Mapped[Optional["Reviewer"]] = relationship(back_populates="approved_contents")

    approved_at: Mapped[Optional[datetime]] = mapped_column(default=None, nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(),index=True)

    topic: Mapped["Topic"] = relationship(back_populates="topic_contents")
