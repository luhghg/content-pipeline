from fastapi import APIRouter, Depends
from app.services.contents_service import get_contents_service
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated
from app.schemas.contents_schemas import ContentItemResponse
from app.models.db_models import Status, ContentType




router = APIRouter(prefix="/content", tags=["/content"])

@router.get(path="/", response_model=List[ContentItemResponse])
async def get_contents(session: Annotated[AsyncSession, Depends(get_session)],
                       status: Status | None = None, type: ContentType | None = None,
                       limit: int = 10, offset: int = 0) -> List[ContentItemResponse]:

    contents = await get_contents_service(session=session, status=status,
                                          type=type, limit=limit, offset=offset)

    return contents 
