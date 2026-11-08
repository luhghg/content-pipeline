from fastapi import APIRouter, Depends
from app.services.contents_service import  get_grouped_items_by_status
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import  Annotated
from app.schemas.contents_schemas import ContentItemResponse
from app.models.db_models import Status



router = APIRouter(prefix="/board", tags=["/board"])

@router.get(path="/" ,response_model=dict[Status, list[ContentItemResponse]])
async def kanban_board(session: Annotated[AsyncSession, Depends(get_session)]) -> dict[Status, list[ContentItemResponse]]:
    result = await get_grouped_items_by_status(session=session)
    return result
