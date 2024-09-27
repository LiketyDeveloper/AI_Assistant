from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

KB_SEND_ASSISTENT_MESSAGE = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отправить", callback_data="send_assistent_message")],
])