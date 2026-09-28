import asyncio
from app.LLM.LLM_service import do_algorythm

if __name__ == "__main__":
    llm_data = asyncio.run(do_algorythm())

    print(llm_data)
