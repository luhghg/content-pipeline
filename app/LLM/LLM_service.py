from app.LLM.LLM_functions import get_llm_provider, Context

async def do_algorythm() -> dict:

    current_provider =  get_llm_provider()

    result = Context(strategy=current_provider)

    return await result.give_information(prompt="Ответь одним словом: привет")
