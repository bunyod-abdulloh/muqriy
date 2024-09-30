from typing import List

from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    Message
)

from bot.keyboards.inline.quran_ibuttons import key_returner_muqriy_husary
from bot.other.functions import extracter
from loader import db

router = Router()


@router.message(F.media_group_id)
async def handle_albums(message: Message, album: List[Message]):
    """This handler will receive a complete album of any type."""
    group_elements = []

    for element in album:
        # caption_kwargs = {"caption": element.caption, "caption_entities": element.caption_entities}
        # if element.photo:
        #     input_media = InputMediaPhoto(media=element.photo[-1].file_id, **caption_kwargs)
        # elif element.video:
        #     input_media = InputMediaVideo(media=element.video.file_id, **caption_kwargs)
        # elif element.document:
        #     input_media = InputMediaDocument(media=element.document.file_id, **caption_kwargs)
        if element.audio:
            for n in range(11):
                sura_number = element.audio.file_name.split(".")[0]
                # await message.answer(
                #     text=f"<code>{element.audio.file_id}</code>\n\n{element.audio.file_name}"
                # )
                print(n)
                await db.update_temp_to_muqriy(
                    audiomuqriy=element.audio.file_id
                )
                # await db.update_edu_to_muqriy(
                #     sequence=sura_number,
                #     audiomuqriy=element.audio.file_id
                # )
        else:
            return message.answer("This media type isn't supported!")


@router.message(F.text == "Qur'oni Karim tilovati (Hasanxon va Husaynxon qorilar)")
async def quran_hasanxon_husaynxon_handler(message: types.Message, state: FSMContext):
    await state.clear()

    muqriy_recitation = await db.select_all_muqriyaudio()

    extract = extracter(
        all_medias=muqriy_recitation, delimiter=10
    )
    current_page = 1
    all_pages = len(extract)

    items = extract[current_page - 1]
    markup = key_returner_muqriy_husary(
        items=items, callback_data="audiomuqriy", current_page=current_page, all_pages=all_pages, selected="001"
    )

    await message.answer_audio(
        audio=items[0]['audiomuqriy'], reply_markup=markup
    )


@router.callback_query(F.data.startswith("select_audiomuqriy:"))
async def quran_hasanxon_husaynxon_selectpts(call: types.CallbackQuery):
    sequence = call.data.split(':')[1]
    current_page = int(call.data.split(':')[2])
    muqriy_recitation = await db.select_all_muqriyaudio()
    get_sura = await db.select_muqriyaudio(
        sequence=sequence
    )
    extract = extracter(
        all_medias=muqriy_recitation, delimiter=10
    )
    items = extract[current_page - 1]
    markup = key_returner_muqriy_husary(
        items=items, callback_data="audiomuqriy", current_page=current_page, all_pages=len(extract), selected=sequence
    )
    await call.message.edit_media(
        media=types.InputMediaAudio(
            media=get_sura['audiomuqriy']
        ), reply_markup=markup
    )


@router.callback_query(F.data.startswith("prev_audiomuqriy:"))
async def quran_hasanxon_husaynxon_prev_pts(call: types.CallbackQuery):
    await call.answer(
        cache_time=0
    )
    current_page = int(call.data.split(':')[2])
    muqriy_recitation = await db.select_all_muqriyaudio()

    extract = extracter(
        all_medias=muqriy_recitation, delimiter=10
    )

    all_pages = len(extract)

    if current_page == 1:
        current_page = all_pages
    else:
        current_page -= 1

    items = extract[current_page - 1]
    markup = key_returner_muqriy_husary(
        items=items, callback_data="audiomuqriy", current_page=current_page, all_pages=len(extract),
        selected=items[-1]['sequence']
    )
    await call.message.edit_media(
        media=types.InputMediaAudio(
            media=items[-1]['audiomuqriy']
        ), reply_markup=markup
    )


@router.callback_query(F.data.startswith("next_audiomuqriy"))
async def quran_hasanxon_husaynxon_next_pts(call: types.CallbackQuery):
    await call.answer(
        cache_time=0
    )
    current_page = int(call.data.split(':')[2])
    muqriy_recitation = await db.select_all_muqriyaudio()

    extract = extracter(
        all_medias=muqriy_recitation, delimiter=10
    )

    all_pages = len(extract)
    
    if current_page == all_pages:
        current_page = 1
    else:
        current_page += 1

    items = extract[current_page - 1]

    markup = key_returner_muqriy_husary(
        items=items, callback_data="audiomuqriy", current_page=current_page, all_pages=len(extract),
        selected=items[0]['sequence']
    )
    await call.message.edit_media(
        media=types.InputMediaAudio(
            media=items[0]['audiomuqriy']
        ), reply_markup=markup
    )


@router.callback_query(F.data.startswith("alert_audiomuqriy"))
async def quran_hasanxon_husaynxon_alert(call: types.CallbackQuery):
    current_page = call.data.split(":")[1]
    await call.answer(
        text=f"Siz {current_page} - sahifadasiz", show_alert=True
    )


@router.callback_query(F.data.startswith("content_audiomuqriy:"))
async def quran_hasanxon_husaynxon_content(call: types.CallbackQuery):
    current_page = int(call.data.split(":")[1])
    muqriy_recitation = await db.select_all_muqriyaudio()
    extract = extracter(
        all_medias=muqriy_recitation, delimiter=10
    )
    items = extract[current_page - 1]

    content = str()

    for item in items:
        content += f"{item['sequence']}. {item['sura_name']} surasi\n"
    await call.answer(
        text=content, show_alert=True
    )
