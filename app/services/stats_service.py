from app.repositories.stats_repo import (get_count_of_approved_items_repo,
                                         get_count_of_automatical_approved_items_repo,
                                         get_list_of_responded_at__and_sent_at_repo,
                                         get_sum_of_tokens_repo,
                                         sum_of_cost_estimate_repo)
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta


async def get_sum_of_tokens_service(session: AsyncSession):
    result = await get_sum_of_tokens_repo(session=session)
    return result


async def sum_of_cost_estimate_service(session: AsyncSession):
    result = await sum_of_cost_estimate_repo(session=session)
    return result


async def dolya_avtoodobreniy_service(session: AsyncSession):
    count_automatical_approved = await get_count_of_approved_items_repo(session=session)
    count_of_automatical_approved = await get_count_of_automatical_approved_items_repo(session=session)
    if count_automatical_approved is not 0 and count_of_automatical_approved is not 0:
        result = (count_of_automatical_approved * 100) / count_automatical_approved
        return result


async def avg_time_of_waiting_service(session: AsyncSession):
    list_of_dates = await get_list_of_responded_at__and_sent_at_repo(session=session)
    list_of_subtraction = []
    for responded_at, sent_at in list_of_dates:
        duration = responded_at - sent_at
        list_of_subtraction.append(duration)
    seconds_list = []
    for d in list_of_subtraction:
        seconds = d.total_seconds()
        seconds_list.append(seconds)
    avg = (sum(seconds_list) / len(seconds_list))
    avg_duration = timedelta(seconds=avg)
    return avg_duration
