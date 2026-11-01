from app.core.config import settings
from arq.connections import RedisSettings
from app.LLM.LLM_service import generate_content, quality_check, request_review, proces_review_desicion, plan_cotent
from app.db.session import async_engine, async_session
from arq import create_pool
from app.models.db_models import Status
from arq.cron import cron


REDIS_SETTINGS = RedisSettings(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


async def startup(ctx):
    ctx["db_factory"] = async_session


async def shutdown(ctx):
    await async_engine.dispose()


async def wrapper_arq_fun(ctx, item_id: int):
    async with ctx["db_factory"]() as session:
         res = await generate_content(session=session, item_id=item_id)
         if res:
             await ctx["redis"].enqueue_job("wrapper_arq_quality_cheker", content_id=item_id)


async def wrapper_arq_quality_cheker(ctx, content_id: int):
    async with ctx["db_factory"]() as session:
        res = await quality_check(session=session, content_id=content_id)
        if res == Status.NEEDS_REVIEW:
            await ctx["redis"].enqueue_job("wrapper_arq_request_review", content_id=content_id)


async def wrapper_arq_request_review(ctx, content_id: int):
    async with ctx["db_factory"]() as session:
        await request_review(session=session, content_id=content_id)

async def wrapper_proces_review_desicion(ctx, content_id: int, callback_data: str, tg_id: int, callback_query_id:str):
    async with ctx["db_factory"]() as session:
            await proces_review_desicion(session=session, content_id=content_id, callback_query_id=callback_query_id, callback_data=callback_data, tg_id=tg_id)

async def wrapper_plan_content(ctx):
    async with ctx["db_factory"]() as session:
        await plan_cotent(session=session)



async def main(item_id: int):
    redis = await create_pool(REDIS_SETTINGS)
    await redis.enqueue_job("wrapper_arq_fun", item_id=item_id)


class WorkerSettings:

    redis_settings = REDIS_SETTINGS

    functions = [wrapper_arq_fun, wrapper_arq_quality_cheker, wrapper_arq_request_review, wrapper_proces_review_desicion, wrapper_plan_content]
    cron_jobs = [
        cron(wrapper_plan_content, second=0)
    ]
    on_startup = startup
    on_shutdown = shutdown
