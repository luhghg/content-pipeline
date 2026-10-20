from fastapi import APIRouter
from app.worker.config import REDIS_SETTINGS
from arq import create_pool

router = APIRouter(prefix="/webhook", tags=["webhook"])



@router.post(path="/telegram")
async def smth(text:dict):
    to_split_callback_data = text["callback_query"]["data"]
    callback_data, content_id = to_split_callback_data.split(":")
    content_id = int(content_id)
    tg_id = text["callback_query"]["from"]["id"]
    callback_query_id = text["callback_query"]["id"]
    redis = await create_pool(REDIS_SETTINGS)
    await redis.enqueue_job("wrapper_proces_review_desicion", tg_id=tg_id, content_id=content_id,
                            callback_data=callback_data, callback_query_id=callback_query_id)
