from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

inline_keyboard = [[
    InlineKeyboardButton(text="✅ Yes", callback_data='yes'),
    InlineKeyboardButton(text="❌ No", callback_data='no')
]]
are_you_sure_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def first_key_returner(items, current_page, all_pages, selected):
    builder = InlineKeyboardBuilder()
    for item in items:
        if selected == item['sequence']:
            builder.add(
                InlineKeyboardButton(
                    text=f"[ {item['sequence']} ]",
                    callback_data=f"select_projects:{item['sequence']}:{current_page}"
                )
            )
        else:
            builder.add(
                InlineKeyboardButton(
                    text=f"{item['sequence']}",
                    callback_data=f"select_pts:{item['sequence']}:{current_page}"
                )
            )
    builder.adjust(5)
    builder.row(
        InlineKeyboardButton(
            text="◀️",
            callback_data=f"prev_pts:{current_page}:{items[0]['sequence']}"
        ),
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data=f"alert_pts:{current_page}"
        ),
        InlineKeyboardButton(
            text="▶️",
            callback_data=f"next_pts:{current_page}:{items[0]['sequence']}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="📖 Mundarija",
            callback_data=f"content_projects:{current_page}:{items[0]['sequence']}"
        )
    )
    return builder.as_markup()
