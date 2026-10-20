from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_models import ReviewRequest
from sqlalchemy import select, desc


async def get_review_request_by_content_id(session: AsyncSession, content_id: int) -> ReviewRequest:
    query = (
        select(ReviewRequest)
        .where(ReviewRequest.content_item_id == content_id)
        .order_by(desc(ReviewRequest.id))
        .limit(1)

    )

    res = await session.execute(query)
    return res.scalar_one_or_none()




