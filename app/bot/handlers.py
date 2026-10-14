from  app.bot.bot import bot
from app.bot.keyboard import inline_keyboard



async def send_message_to_check(chat_id: int, text: str):
    message =  await bot.send_message(chat_id=chat_id,
                                      text=text,
                                      reply_markup=inline_keyboard
                                     )
    return message
