from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_models import LLMCall, ContentItem, Status, ApprovalType, ReviewRequest
from sqlalchemy import select, func, asc




async def get_sum_of_tokens_repo(session: AsyncSession):
    query = (
        select(func.sum(LLMCall.prompt_tokens + LLMCall.completion_tokens))
    )
    result = await session.execute(query)
    return result.scalar()


async def sum_of_cost_estimate_repo(session: AsyncSession):
    query = (
        select(func.sum(LLMCall.cost_estimate))
    )
    result = await session.execute(query)
    return result.scalar()


async def get_count_of_approved_items_repo(session: AsyncSession):
    query = (
        select(func.count(ContentItem.id))
        .where(ContentItem.status == Status.APPROVED)
    )
    result = await session.execute(query)
    return result.scalar()

async def get_count_of_automatical_approved_items_repo(session: AsyncSession):
    query =(
        select(func.count(ContentItem.id))
        .where(ContentItem.status == Status.APPROVED,
               ContentItem.approval_type == ApprovalType.AUTOMATIC)
    )

    result = await session.execute(query)
    return result.scalar()


async def get_list_of_responded_at__and_sent_at_repo(session: AsyncSession):
    query = (
        select(ReviewRequest.responded_at, ReviewRequest.sent_at)
        .where(ReviewRequest.responded_at != None)
        .order_by(asc(ReviewRequest.id))
    )
    res = await session.execute(query)
    return res.all()
