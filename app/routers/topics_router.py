from fastapi import APIRouter, Depends
from app.services.topics_service import create_topic_service
from app.schemas.topics_schemas import TopicResponse, TopicCreate
from app.db.session import get_session
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/topics", tags=["topics"])

@router.post(path="/", response_model=TopicResponse)
async def create_topic(data: TopicCreate, session: Annotated[AsyncSession, Depends(get_session)]) -> TopicResponse:
    new_topic = await create_topic_service(session=session, data=data)
    return new_topic
