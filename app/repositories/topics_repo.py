from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.topics_schemas import TopicCreate
from app.models.db_models import Topic
from sqlalchemy import select, asc, nullsfirst

async def create_topic_repo(session: AsyncSession, data: TopicCreate) -> Topic:

    new_topic = Topic(title=data.title,
                      content_type=data.content_type,
                      prompt_hint=data.prompt_hint,
                    )

    session.add(new_topic)
    await session.commit()
    await session.refresh(new_topic)
    return new_topic


async def serch_the_last_one_active_topic_repo(session:AsyncSession, content_type:str):
    query = (
        select(Topic)
        .where(Topic.content_type == content_type)
        .where(Topic.is_active == True)
        .order_by(asc(Topic.last_used_at).nullsfirst())
        .limit(1)
    )
    res = await session.execute(query)
    return res.scalar_one_or_none()
