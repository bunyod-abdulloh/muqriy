from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def qurantanishuv_buttons(callback: str):
    builder = InlineKeyboardBuilder()

    for button in range(26):
        builder.add(
            InlineKeyboardButton(
                text=f"{button+1}",
                callback_data=f"{callback}:{button+1}"
            )
        )
    builder.adjust(5)
    builder.row(
        InlineKeyboardButton(
            text="⬅️ Ortga", callback_data="qurantanishuv_back"
        ),
        InlineKeyboardButton(
            text="Mundarija", web_app=WebAppInfo(
                url="https://telegra.ph/Quron-bilan-tanishuv-09-30"
            )
        )
    )
    return builder.as_markup()
