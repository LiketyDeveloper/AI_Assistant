from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_operator_menu(is_working):
    if not is_working:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Начать", callback_data="operator|start_support")]
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Остановить", callback_data="operator|stop_support")]
        ])
