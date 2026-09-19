from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.topics_schemas import TopicCreate, TopicResponse
from app.repositories.topics_repo import create_topic_repo


async def create_topic_service(session: AsyncSession, data: TopicCreate) -> TopicResponse:
    new_topic = await create_topic_repo(session=session, data=data)
    new_topic_res = TopicResponse(id=new_topic.id,
                                  title=new_topic.title,
                                  content_type=new_topic.content_type,
                                  is_active=new_topic.is_active,
                                  last_used_at=new_topic.last_used_at,
                                  created_at=new_topic.created_at
                                 )
    return new_topic_res
