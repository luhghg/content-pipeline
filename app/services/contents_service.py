from app.repositories.contents_repo import get_contents_repo
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_models import ContentItem, ContentType, Status
from typing import Sequence




async def get_contents_service(session: AsyncSession, status: Status | None = None, type: ContentType | None = None,
                            limit: int = 10, offset: int = 0) -> Sequence[ContentItem]:
    contents = await get_contents_repo(session=session, status=status,
                                       type=type, limit=limit, offset=offset)

    return contents
