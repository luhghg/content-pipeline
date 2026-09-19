from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.topics_schemas import TopicCreate
from app.models.db_models import Topic


async def create_topic_repo(session: AsyncSession, data: TopicCreate) -> Topic:

    new_topic = Topic(title=data.title,
                      content_type=data.content_type,
                      prompt_hint=data.prompt_hint,
                    )

    session.add(new_topic)
    await session.commit()
    await session.refresh(new_topic)
    return new_topic
