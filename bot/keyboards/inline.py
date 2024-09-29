from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

KB_SEND_ASSISTENT_MESSAGE = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="1️⃣", callback_data="send_assistent_message|1"),
        InlineKeyboardButton(text="2️⃣", callback_data="send_assistent_message|2"),
        InlineKeyboardButton(text="3️⃣", callback_data="send_assistent_message|3"),
    ]
])



KB_EMPTY = InlineKeyboardMarkup(inline_keyboard=[[]])