from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

inline_keyboard = [[
    InlineKeyboardButton(text="✅ Yes", callback_data='yes'),
    InlineKeyboardButton(text="❌ No", callback_data='no')
]]
are_you_sure_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def key_returner_muqriy_husary(items, callback_data, current_page, all_pages, selected=None):
    builder = InlineKeyboardBuilder()
    for item in items:
        if selected == item['sequence']:
            builder.add(
                InlineKeyboardButton(
                    text=f"[ {item['sequence']} ]",
                    callback_data=f"selected_{callback_data}:{item['sequence']}:{current_page}"
                )
            )
        else:
            builder.add(
                InlineKeyboardButton(
                    text=f"{item['sequence']}",
                    callback_data=f"select_{callback_data}:{item['sequence']}:{current_page}"
                )
            )
    builder.adjust(4)
    builder.row(
        InlineKeyboardButton(
            text="◀️",
            callback_data=f"prev_{callback_data}:{items[0]['sequence']}:{current_page}"
        ),
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data=f"alert_{callback_data}:{current_page}"
        ),
        InlineKeyboardButton(
            text="▶️",
            callback_data=f"next_{callback_data}:{items[0]['sequence']}:{current_page}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="📖 Mundarija",
            callback_data=f"content_{callback_data}:{current_page}"
        )
    )
    return builder.as_markup()


def quran_next_prev_ibuttons(sura_audio, sura_photo, ayah_audio, ayah_photo, total_verses):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="⬅️ Oldingi",
                callback_data=f"husaryprev_{sura_audio}_{sura_photo}_{ayah_audio}_{ayah_photo}_{total_verses}"
            ),
            InlineKeyboardButton(
                text="Keyingi ➡️",
                callback_data=f"husarynext_{sura_audio}_{sura_photo}_{ayah_audio}_{ayah_photo}_{total_verses}"
            )
        ]]
    )
    return markup


def quran_prev_ibutton(sura_audio, sura_photo, ayah_audio, ayah_photo, total_verses):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="⬅️ Oldingi",
                callback_data=f"husaryprev_{sura_audio}_{sura_photo}_{ayah_audio}_{ayah_photo}_{total_verses}"
            )
        ]]
    )
    return markup


def quran_next_ibutton(sura_audio, sura_photo, ayah_audio, ayah_photo, total_verses):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="Keyingi ➡️",
                callback_data=f"husarynext_{sura_audio}_{sura_photo}_{ayah_audio}_{ayah_photo}_{total_verses}"
            )
        ]]
    )
    return markup
