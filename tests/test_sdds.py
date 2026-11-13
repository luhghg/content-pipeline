from app.models.db_models import ContentItem, Topic, ContentType, Status, Reviewer
from app.LLM.LLM_service import quality_check, proces_review_desicion, request_review
from tests.conftest import Zaglushka, fake_send_message_to_check, fake_answer_callback, fake_remove_buttons



async def test_smth(monkeypatch, db_session):
    topic = Topic(title="hello world",
                  content_type=ContentType.ARTICLE
                  )
    db_session.add(topic)
    await db_session.commit()


    content_item = ContentItem(topic_id=topic.id,
                               content_type=topic.content_type,
                               status=Status.CHECKING
                              )

    db_session.add(content_item)
    await db_session.commit()

    reviewer = Reviewer(telegram_id=1,
                        username="vova")
    db_session.add(reviewer)
    await db_session.commit()


    monkeypatch.setattr("app.LLM.LLM_service.get_llm_provider", Zaglushka)

    res = await quality_check(session=db_session, content_id=content_item.id)

    monkeypatch.setattr("app.LLM.LLM_service.send_message_to_check", fake_send_message_to_check)

    await request_review(session=db_session, content_id=content_item.id)

    monkeypatch.setattr("app.LLM.LLM_service.answer_callback", fake_answer_callback)

    monkeypatch.setattr("app.LLM.LLM_service.remove_buttons", fake_remove_buttons)

    await proces_review_desicion(session=db_session, content_id=content_item.id, callback_data = "accept", tg_id=1, callback_query_id="1234")

    assert content_item.status == Status.APPROVED
