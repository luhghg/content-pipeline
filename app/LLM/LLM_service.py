from app.services.contents_service import get_content_item_by_id_service
from app.prompts.content_item_title_body_prompt import title_body_prompt
from sqlalchemy.ext.asyncio import AsyncSession
from app.LLM.LLM_functions import get_llm_provider, Context
from app.models.db_models import LLMCall, Purpose
from app.core.config import settings
import time
import json
from app.models.db_models import  Status


current_model = settings.MODEL_NAME

async def generate_content(session: AsyncSession, item_id: int):
    content = await get_content_item_by_id_service(session=session, id=item_id)
    prompt = title_body_prompt(title=content.topic.title,
                               content_type=content.content_type,
                               prompt_hint=content.topic.prompt_hint
                               )
    current_provider =  get_llm_provider()

    result = Context(strategy=current_provider)
    start = time.perf_counter()
    try:
        response = await result.give_information(prompt=prompt)
        parsed = json.loads(response["text"])
        content_title = parsed["title"]
        content_body = parsed["body"]

        llm_call_model = LLMCall(content_item_id=item_id,
                                 purpose=Purpose.GENERATION,
                                 model=response["model"],
                                 prompt_tokens=response["prompt_tokens"],
                                 completion_tokens=response["completion_tokens"],
                                 cost_estimate=response["cost_estimate"],
                                 latency_ms=response["latency_ms"],
                                 attempt=1,
                                 succeeded=True,
                                )
        content.title = content_title
        content.body = content_body
        content.status = Status.CHECKING

        session.add(llm_call_model)
        await session.commit()

    except Exception as e:
        finish_time = round((time.perf_counter() - start) * 1000)
        llm_call_model = LLMCall(
                                content_item_id=item_id,
                                purpose=Purpose.GENERATION,
                                model=current_model,
                                prompt_tokens=None,
                                completion_tokens=None,
                                cost_estimate=None,
                                latency_ms=finish_time,
                                attempt=1,
                                error=str(e),
                                succeeded=False
                                )

        session.add(llm_call_model)
        await session.commit()
