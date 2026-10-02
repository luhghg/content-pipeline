import asyncio
from app.LLM.LLM_checker import do_algorythm, testim_generate
from app.LLM.LLM_service import generate_content
from app.db.session import async_session

if __name__ == "__main__":
    llm_data = asyncio.run(testim_generate(id=1))


    print(llm_data)
