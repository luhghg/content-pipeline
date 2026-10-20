from  app.bot.bot import bot
from app.bot.keyboard import rej_acc_keyboard



async def send_message_to_check(chat_id: int, text: str, item_id: int):
    message =  await bot.send_message(chat_id=chat_id,
                                      text=text,
                                      reply_markup=rej_acc_keyboard(item_id=item_id)
                                     )
    return message


async def answer_callback(callback_query_id: str, text: str):
    await bot.answer_callback_query(callback_query_id=callback_query_id, text=text)


async def remove_buttons(chat_id: int, message_id: int, text:str):
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=None,
                                text = text)
