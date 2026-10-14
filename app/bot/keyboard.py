
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отклонить❌' ,callback_data="reject")],
    [InlineKeyboardButton(text='Одобрить✅', callback_data="accept")]

])
