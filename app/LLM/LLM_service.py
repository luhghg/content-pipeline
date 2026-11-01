from app.services.contents_service import get_content_item_by_id_service
from app.prompts.content_item_title_body_prompt import title_body_prompt
from sqlalchemy.ext.asyncio import AsyncSession
from app.LLM.LLM_functions import get_llm_provider, Context
from app.models.db_models import LLMCall, Purpose, QualityCheck
from app.core.config import settings
import time
import json
import asyncio
from app.models.db_models import  Status, Verdict, ApprovalType, ReviewRequest, Desicion, ContentItem
from app.prompts.checker_prompt import to_check
from datetime import datetime
from app.LLM.LLM_functions import transition
from app.repositories.quality_check_repo import get_quality_check_by_content_item_id
from app.bot.handlers import send_message_to_check
from app.repositories.review_request_repo import get_review_request_by_content_id
from app.bot.handlers import answer_callback, remove_buttons
from app.repositories.reviewer_repo import get_reviewer_by_telegram_id
from app.repositories.schedule_rules_repo import get_schedule_rules_repo
from app.repositories.topics_repo import serch_the_last_one_active_topic_repo
from croniter import croniter

current_model = settings.MODEL_NAME

async def generate_content(session: AsyncSession, item_id: int):
    content = await get_content_item_by_id_service(session=session, id=item_id)
    if content.status != Status.QUEUED:
        return False
    prompt = title_body_prompt(title=content.topic.title,
                               content_type=content.content_type,
                               prompt_hint=content.topic.prompt_hint
                               )
    current_provider =  get_llm_provider()

    result = Context(strategy=current_provider)
    start = time.perf_counter()
    try:
        transition(item=content, new_status=Status.GENERATING)
        for one_try in range(1,4):
            try:
                response = await result.give_information(prompt=prompt)
                break
            except Exception as e :
                if one_try == 1:
                    await asyncio.sleep(1)
                elif one_try == 2:
                    await asyncio.sleep(4)
                elif one_try == 3:
                    await asyncio.sleep(16)
                llmcall_obj = LLMCall(content_item_id=item_id,
                                                purpose=Purpose.GENERATION,
                                                model=current_model,
                                                prompt_tokens=None,
                                                completion_tokens=None,
                                                cost_estimate=None,
                                                latency_ms=0,
                                                attempt=one_try,
                                                error=str(e),
                                                succeeded=False)
                session.add(llmcall_obj)
                await session.commit()


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
                                 attempt=one_try,
                                 succeeded=True,
                                )
        content.title = content_title
        content.body = content_body
        transition(item=content, new_status=Status.CHECKING)

        session.add(llm_call_model)
        await session.commit()
        return True

    except Exception as e:
        await session.rollback()
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
        return False






async def quality_check(session: AsyncSession, content_id: int):
    content = await get_content_item_by_id_service(session=session, id=content_id)
    prompt =  to_check(text=content.body)

    current_provider =  get_llm_provider()

    result = Context(strategy=current_provider)
    start = time.perf_counter()
    try:
        for one_try in range(1,4):
            try:
                response = await result.give_information(prompt=prompt)
                break
            except Exception as e:
                if one_try == 1:
                    await asyncio.sleep(1)
                elif one_try == 2:
                    await asyncio.sleep(4)
                elif one_try == 3:
                    await asyncio.sleep(16)
                llmcall_obj = LLMCall(content_item_id=content.id,
                                    purpose=Purpose.QUALITYCHECK,
                                    model=current_model,
                                    prompt_tokens=None,
                                    completion_tokens=None,
                                    cost_estimate=None,
                                    latency_ms=0,
                                    attempt=one_try,
                                    error=str(e),
                                    succeeded=False)
                session.add(llmcall_obj)
                await session.commit()


        parsed = json.loads(response["text"])
        verdict = Verdict(parsed["verdict"])
        score = parsed["score"]
        reasons = parsed["reasons"]
        llm_call_model = LLMCall(content_item_id=content_id,
                                 purpose=Purpose.QUALITYCHECK,
                                 model=response["model"],
                                 prompt_tokens=response["prompt_tokens"],
                                 completion_tokens=response["completion_tokens"],
                                 cost_estimate=response["cost_estimate"],
                                 latency_ms=response["latency_ms"],
                                 attempt=one_try,
                                 succeeded=True,
                                )
        if verdict == Verdict.PASS:
            transition(item=content, new_status=Status.APPROVED)
            content.approval_type = ApprovalType.AUTOMATIC
            content.approved_at = datetime.now()
        elif verdict == Verdict.DOUBTFUL:
           transition(item=content, new_status=Status.NEEDS_REVIEW)

        qc = QualityCheck(content_item_id=content_id,
                          verdict=verdict,
                          score=score,
                          reasons=reasons)

        session.add(llm_call_model)
        session.add(qc)
        await session.commit()
        return content.status

    except Exception as e:
        await session.rollback()
        await session.refresh(content)
        finish_time = round((time.perf_counter() - start) * 1000)
        llm_call_model = LLMCall(
                                 content_item_id=content_id,
                                 purpose=Purpose.QUALITYCHECK,
                                 model=current_model,
                                 prompt_tokens=None,
                                 completion_tokens=None,
                                 cost_estimate=None,
                                 latency_ms=finish_time,
                                 attempt=1,
                                 error=str(e),
                                 succeeded=False
                                )
        qc = QualityCheck(content_item_id=content_id,
                                  verdict=Verdict.FAIL,
                                  score=None,
                                  reasons=None)

        transition(item=content, new_status=Status.NEEDS_REVIEW)

        session.add(llm_call_model)
        session.add(qc)
        await session.commit()
        return content.status




async def request_review(session: AsyncSession, content_id: int):
    content = await get_content_item_by_id_service(session=session, id=content_id)
    quality = await get_quality_check_by_content_item_id(session=session, content_id=content.id)
    message = f"title: {content.title}, body: {content.body}, reasons: {quality.reasons}"
    send_message = await send_message_to_check(chat_id=settings.CHAT_ID, text=message, item_id=content_id)
    print(f"send_message{send_message}")
    review_request = ReviewRequest(content_item_id=content.id,
                                   telegram_chat_id=send_message.chat.id,
                                   telegram_message_id=send_message.message_id,
                                   sent_at=datetime.now(),
                                   )
    session.add(review_request)
    await session.commit()




async def proces_review_desicion(session: AsyncSession, content_id: int, callback_data: str, tg_id: int, callback_query_id:str):
    review_request = await get_review_request_by_content_id(session=session, content_id=content_id)
    content = await get_content_item_by_id_service(session=session, id=content_id)
    if review_request.responded_at is not None:
        await answer_callback(callback_query_id=callback_query_id ,text="Already processed")
        return
    elif review_request.responded_at is None:
        if callback_data == "accept":
            await answer_callback(callback_query_id=callback_query_id, text="The article has been successfully approved!")
            transition(item=content, new_status=Status.APPROVED)
            content.approval_type = ApprovalType.MANUAL
            res_by_id = await get_reviewer_by_telegram_id(session=session, telegram_id=tg_id)
            content.approved_by_id = res_by_id.id
            review_request.responded_at = datetime.now()
            review_request.desicion = Desicion.APPROVED
            review_request.reviewer_telegram_id = tg_id
            await remove_buttons(chat_id=review_request.telegram_chat_id,
                                 message_id=review_request.telegram_message_id,
                                 text="✅Approved")

            await session.commit()

        elif callback_data == "reject":
            await answer_callback(callback_query_id=callback_query_id ,text="The article has been successfully rejected!")
            transition(item=content, new_status=Status.REJECTED)
            content.approval_type = ApprovalType.MANUAL
            res_by_id = await get_reviewer_by_telegram_id(session=session, telegram_id=tg_id)
            content.approved_by_id = res_by_id.id
            review_request.responded_at = datetime.now()
            review_request.desicion = Desicion.REJECTED
            review_request.reviewer_telegram_id = tg_id
            await remove_buttons(chat_id=review_request.telegram_chat_id,
                                message_id=review_request.telegram_message_id,
                                text="❌Rejected")

            await session.commit()


async def plan_cotent(session: AsyncSession):
    rules =  await get_schedule_rules_repo(session=session)
    for rule in rules:
        for _ in range(1, rule.items_per_run + 1):
            topic = await serch_the_last_one_active_topic_repo(session=session, content_type=rule.content_type)
            if topic is not None:
                new_content = ContentItem(topic_id=topic.id,
                                          content_type=topic.content_type,
                                          status=Status.QUEUED,
                                         )
                topic.last_used_at = datetime.now()
                session.add(new_content)
        calculator = croniter(rule.cron_expression, datetime.now())
        rule.next_launch = calculator.get_next(datetime)
    await session.commit()
    
