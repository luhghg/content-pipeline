from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_models import QualityCheck
from sqlalchemy import select

async def get_quality_check_by_content_item_id(session: AsyncSession, content_id: int) -> QualityCheck:
    query = (
        select(QualityCheck)
        .where(QualityCheck.content_item_id == content_id)
    )
    res = await session.execute(query)
    return res.scalar_one_or_none()
