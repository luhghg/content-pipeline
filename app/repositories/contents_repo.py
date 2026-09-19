from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from app.models.db_models import ContentItem
from sqlalchemy import select
from app.models.db_models import Status, ContentType



async def get_contents_repo(session: AsyncSession, status: Status | None = None, type: ContentType | None = None,
                            limit: int = 10, offset: int = 0  ) -> Sequence[ContentItem]:
    query=(
           select(ContentItem)
          )
    if status is not None:
        query = query.where(ContentItem.status == status)

    if type is not None:
        query = query.where(ContentItem.content_type == type)

    query = query.limit(limit=limit).offset(offset=offset)

    result = await session.execute(query)
    return result.scalars().all()
