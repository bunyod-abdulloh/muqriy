from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def audio_video_ibuttons(callback: str):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="🔈 Audio", callback_data=f"audio:{callback}"
            ),
            InlineKeyboardButton(
                text="🎞 Video", callback_data=f"video:{callback}"
            )
        ],
            [
                InlineKeyboardButton(
                    text="🏡 Bosh sahifa", callback_data="back_main"
                )
            ]]
    )
    return markup


def back_ibutton(callback: str):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="⬅️ Ortga", callback_data=callback
            )
        ]]
    )
    return markup
