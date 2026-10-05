import asyncio
from app.LLM.LLM_checker import do_algorythm, testim_generate
from app.LLM.LLM_service import generate_content
from app.db.session import async_session
from app.worker.config import main

if __name__ == "__main__":
    llm_data = asyncio.run(main(1))


    print(llm_data)
