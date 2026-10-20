from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_models import Reviewer


async def get_reviewer_by_telegram_id(session:AsyncSession, telegram_id: int) -> Reviewer:
    query =(
        select(Reviewer)
        .where(Reviewer.telegram_id == telegram_id)

    )
    res = await session.execute(query)
    return res.scalar_one_or_none()
