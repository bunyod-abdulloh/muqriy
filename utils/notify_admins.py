import logging

from aiogram import Bot

from data.config import ADMIN_ID


async def on_startup_notify(bot: Bot):
    try:
        bot_properties = await bot.me()
        message = ["<b>Bot ishga tushdi.</b>\n",
                   f"<b>Bot ID:</b> {bot_properties.id}",
                   f"<b>Bot Username:</b> {bot_properties.username}"]
        await bot.send_message(chat_id=ADMIN_ID,
                               text="\n".join(message))
    except Exception as err:
        logging.exception(err)
