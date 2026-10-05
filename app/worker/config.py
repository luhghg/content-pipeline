from app.core.config import settings
from arq.connections import RedisSettings
from app.LLM.LLM_service import generate_content
from app.db.session import async_engine, async_session
from arq import create_pool



REDIS_SETTINGS = RedisSettings(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


async def startup(ctx):
    ctx["db_factory"] = async_session


async def shutdown(ctx):
    await async_engine.dispose()


async def wrapper_arq_fun(ctx, item_id: int):
    async with ctx["db_factory"]() as session:
        await generate_content(session=session, item_id=item_id)


async def main(item_id: int):
    redis = await create_pool(REDIS_SETTINGS)
    await redis.enqueue_job("wrapper_arq_fun", item_id)


class WorkerSettings:

    redis_settings = REDIS_SETTINGS

    functions = [wrapper_arq_fun]

    on_startup = startup
    on_shutdown = shutdown
