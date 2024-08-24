from aiogram import Router, F, types

from bot.keyboards.inline.buttons import first_key_returner
from bot.keyboards.reply.user_main import quran_main_buttons
from bot.other.functions import extracter
from loader import db

router = Router()


@router.message(F.text == "📖 Qur'oni Karim")
async def quran_main_handler(message: types.Message):
    await message.answer(
        text=message.text, reply_markup=quran_main_buttons()
    )


@router.message(F.text == "Qur'oni Karim tilovati (Hasanxon va Husaynxon qorilar)")
async def quran_hasanxon_husaynxon_handler(message: types.Message):
    muqriy_recitation = await db.select_all_muqriyaudio()

    extract = extracter(
        all_medias=muqriy_recitation, delimiter=10
    )
    current_page = 1
    all_pages = len(extract)

    items = extract[current_page - 1]
    markup = first_key_returner(
        items=items, current_page=current_page, all_pages=all_pages, selected=1
    )

    await message.answer_audio(
        audio=items[0]['audiomuqriy'], reply_markup=markup
    )
