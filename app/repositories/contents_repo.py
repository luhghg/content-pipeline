from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from app.schemas.contents_schemas import ContentItemUpdate
from sqlalchemy import select, update
from app.models.db_models import Status, ContentType, ContentItem
from sqlalchemy.orm import selectinload



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



async def get_content_item_by_id_repo(session: AsyncSession, id: int) -> ContentItem | None:
    query = (
        select(ContentItem)
        .where(ContentItem.id == id)
        .options(selectinload(ContentItem.topic))
    )

    result = await session.execute(query)
    return result.scalar_one_or_none()

