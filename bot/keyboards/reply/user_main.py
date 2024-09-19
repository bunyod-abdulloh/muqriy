from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from utils.dicts.dicts import main_menu_buttontxt, quran_main_buttontxt


def main_menu_buttons():
    btns = ReplyKeyboardBuilder()
    for markup in main_menu_buttontxt:
        btns.button(
            text=markup
        )
    btns.adjust(2, 1, repeat=True)
    return btns.as_markup(
        resize_keyboard=True
    )


def quran_main_buttons():
    btns = ReplyKeyboardBuilder()
    for markup in quran_main_buttontxt:
        btns.button(
            text=markup
        )
    btns.button(
        text="Bosh sahifa")
    btns.adjust(2, 1, repeat=True)
    return btns.as_markup(
        resize_keyboard=True, one_time_keyboard=True
    )
