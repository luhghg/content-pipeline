from app.LLM.LLM_functions import get_llm_provider, Context
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session
from app.LLM.LLM_service import generate_content
async def do_algorythm() -> dict:

    current_provider =  get_llm_provider()

    result = Context(strategy=current_provider)

    return await result.give_information(prompt="Ответь одним словом: привет")


async def testim_generate(id: int =1):
    async with async_session() as session:
        await generate_content(session=session, item_id=id)
