from  app.bot.bot import bot
from app.bot.keyboard import rej_acc_keyboard



async def send_message_to_check(chat_id: int, text: str, item_id: int):
    message =  await bot.send_message(chat_id=chat_id,
                                      text=text,
                                      reply_markup=rej_acc_keyboard(item_id=item_id)
                                     )
    return message
