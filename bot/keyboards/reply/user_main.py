from aiogram.utils.keyboard import ReplyKeyboardBuilder

from utils.dicts.dicts import main_menu_buttontxt, quran_main_buttontxt


def main_menu_buttons():
    buttons = ReplyKeyboardBuilder()
    for markup in main_menu_buttontxt:
        buttons.button(
            text=markup
        )
    buttons.adjust(2, 1, repeat=True)
    return buttons.as_markup(
        resize_keyboard=True
    )


def quran_main_buttons():
    buttons = ReplyKeyboardBuilder()
    for markup in quran_main_buttontxt:
        buttons.button(
            text=markup
        )
    buttons.button(
        text="Bosh sahifa"
    )
    buttons.adjust(2, 1, repeat=True)
    return buttons.as_markup(
        resize_keyboard=True
    )
