from fastapi import APIRouter, Depends
from app.services.stats_service import (get_sum_of_tokens_service,
                                        sum_of_cost_estimate_service,
                                        dolya_avtoodobreniy_service,
                                        avg_time_of_waiting_service)
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import  Annotated



router = APIRouter(prefix="/stats", tags=["/stats"])

@router.get(path="/" ,response_model=dict)
async def stats_router(session: Annotated[AsyncSession, Depends(get_session)]) -> dict:
    tokens = await get_sum_of_tokens_service(session=session)
    cost_estiminate = await sum_of_cost_estimate_service(session=session)
    percent = await dolya_avtoodobreniy_service(session=session)
    avg = await avg_time_of_waiting_service(session=session)
    result ={"How many tokens are spent on clicks" : tokens,
            "How much money are spent on clicks" : cost_estiminate,
            "Percent of AUTOMATICAL APPROVE": percent,
            "AVG time of waiting response from admin to approve/reject" : avg}
    return result
