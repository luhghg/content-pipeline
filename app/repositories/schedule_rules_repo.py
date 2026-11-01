from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.db_models import ScheduleRule
from datetime import datetime


async def get_schedule_rules_repo(session: AsyncSession):
    query = (
        select(ScheduleRule)
        .where(ScheduleRule.is_active == True,
               ScheduleRule.next_launch <= datetime.now()
              )
    )

    res = await session.execute(query)
    return res.scalars().all()
