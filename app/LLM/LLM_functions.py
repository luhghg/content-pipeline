from abc import ABC, abstractmethod
from groq import AsyncGroq
from app.core.config import settings

import time


model_entry = settings.MODEL_ENTRY
model_exit = settings.MODEL_EXIT
model_name = settings.MODEL_NAME

client = AsyncGroq(
                  api_key=settings.GROQ_API_KEY
                  )


class Strategy(ABC):

    @abstractmethod
    async def generate(self, prompt: str) -> dict :
        pass



class Context():

    def __init__(self, strategy: Strategy):

        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:

        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:

        self._strategy = strategy

    async def give_information(self, prompt) -> dict:
        result = await self._strategy.generate(prompt=prompt)
        return result



class GroqProvider(Strategy):

    async def generate(self, prompt: str) -> dict:

        t0 = time.perf_counter()
        response = await client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        elapsed_one = round((time.perf_counter() - t0) * 1000)

        p_tokens = response.usage.prompt_tokens
        c_tokens = response.usage.completion_tokens
        cost_estimate = p_tokens * model_entry / 1_000_000 + c_tokens * model_exit / 1_000_000

        answer =  {
                  "model": model_name,
                  "prompt_tokens": p_tokens,
                  "completion_tokens": c_tokens,
                  "cost_estimate": cost_estimate,
                  "latency_ms": elapsed_one * 1000
                  }
        return answer



def get_llm_provider() -> Strategy:

    provider_name = settings.LLM_PROVIDER

    if provider_name == "groq":
        return GroqProvider()

    raise ValueError(f"Unknown provider {provider_name}")
