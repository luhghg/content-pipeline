from app.bot.bot import bot
import asyncio


async def get_chat_id():
    updates = await bot.get_updates()
    print (f"client_chat_id: {updates}")

if __name__ == "__main__":
    llm_data = asyncio.run(get_chat_id())
