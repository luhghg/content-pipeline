
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



def rej_acc_keyboard(item_id: int):
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отклонить❌' ,callback_data=f"reject:{item_id}")],
    [InlineKeyboardButton(text='Одобрить✅', callback_data=f"approve:{item_id}")]])

    return inline_keyboard
