from alembic.config import Config
from app.core.config import settings
from alembic import command
import pytest
from sqlalchemy.ext.asyncio import (AsyncSession, create_async_engine,
                                    async_sessionmaker
                                    )
from app.LLM.LLM_functions import Strategy
import json
from sqlalchemy import create_engine, text

@pytest.fixture(scope="session")
def prepare_database():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.TEST_DATABASE_URL_psycopg)
    command.upgrade(alembic_cfg, "head")
    yield
    engine = create_engine(url=settings.TEST_DATABASE_URL_psycopg)
    with engine.connect() as conn:
        conn.execute(text('DROP SCHEMA public CASCADE;'))
        conn.execute(text('CREATE SCHEMA public;'))
        conn.commit()





@pytest.fixture()
async def db_session(prepare_database):
    async_engine = create_async_engine(url=settings.TEST_DATABASE_URL_asyncpg, echo=True)
    async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


class Zaglushka(Strategy):

    async def generate(self, prompt: str) -> dict:
        answer =  {
                  "model": "fake-model",
                  "prompt_tokens": 1,
                  "completion_tokens": 1,
                  "cost_estimate": 1,
                  "latency_ms": 1,
                  "text": json.dumps({"verdict": "doubtful", "score": 50, "reasons": "..."})
                  }
        return answer



async def fake_send_message_to_check(chat_id: int, text: str ,item_id: int):
    class Fake():
        def __init__(self):
            self.id = 123
    chat = Fake()
    class FakeRes():
        def __init__(self):
            self.chat = chat
            self.message_id = 123
    send_message = FakeRes()
    return send_message


async def fake_answer_callback(callback_query_id: str, text: str):
    return


async def fake_remove_buttons(chat_id: int, message_id: int, text: str):
    return
