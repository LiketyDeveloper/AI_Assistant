from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

KB_STOP_CONN = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Остановить соединение")]
], resize_keyboard=True, one_time_keyboard=True)