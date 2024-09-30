from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.handlers.quran.muqriyrecitation_hr import quran_hasanxon_husaynxon_alert, quran_hasanxon_husaynxon_content
from bot.keyboards.inline.quran_ibuttons import key_returner_muqriy_husary, quran_next_ibutton, quran_prev_ibutton, \
    quran_next_prev_ibuttons
from bot.other.functions import extracter
from bot.states.user_states import Husary
from loader import db
from utils.dicts.dicts import husary_dict

router = Router()


@router.message(F.text == "husary")
async def husary_handler(message):
    """
    Husary Ta'lim uslubida bo'limi bilan bog'liq sura va oyatlar ro'yxatini qo'shish uchun handler.
    """

    c = 0
    for k, v in husary_dict.items():
        c += 1
        sura_name = k
        sequence = v['tartib_raqam']
        audio_id = v['audio']
        zip_id = v['zip']
        total_verses = v['oyat_soni']
        await db.add_quranedu(
            sequence=sequence,
            sura_name=sura_name,
            total_verses=total_verses,
            zip_id=zip_id,
            audiohusary=audio_id
        )
    await message.answer(f"{c} ta ma'lumot qo'shildi!")


@router.message(F.text == "Qur'oni Karim tilovati (ta'lim uslubida)")
async def husary_first_rtr(message: types.Message, state: FSMContext):
    await state.clear()

    husary = await db.select_all_husary()

    extract = extracter(
        all_medias=husary, delimiter=10
    )

    current_page = 1
    all_pages = len(extract)

    items = extract[current_page - 1]
    markup = key_returner_muqriy_husary(
        items=items, callback_data="husary", current_page=current_page, all_pages=all_pages
    )
    await message.answer(
        text="Sura tartib raqamini tanlang", reply_markup=markup
    )


@router.callback_query(F.data.startswith('prev_husary:'))
async def husary_main_prev_rtr(call: types.CallbackQuery):
    await call.answer(
        cache_time=0
    )
    sequence = call.data.split(':')[1]
    current_page = int(call.data.split(':')[2])

    husary = await db.select_all_husary()

    extract = extracter(
        all_medias=husary, delimiter=10
    )

    all_pages = len(extract)

    if current_page == 1:
        current_page = all_pages
    else:
        current_page -= 1

    items = extract[current_page - 1]
    markup = key_returner_muqriy_husary(
        items=items, callback_data="husary", current_page=current_page, all_pages=len(extract)

    )
    await call.message.edit_reply_markup(
        reply_markup=markup
    )


@router.callback_query(F.data.startswith("next_husary:"))
async def husary_main_next_rtr(call: types.CallbackQuery):
    await call.answer(
        cache_time=0
    )
    current_page = int(call.data.split(':')[2])
    husary = await db.select_all_husary()

    extract = extracter(
        all_medias=husary, delimiter=10
    )

    all_pages = len(extract)

    if current_page == all_pages:
        current_page = 1
    else:
        current_page += 1

    items = extract[current_page - 1]

    markup = key_returner_muqriy_husary(
        items=items, callback_data="husary", current_page=current_page, all_pages=len(extract)

    )
    await call.message.edit_reply_markup(
        reply_markup=markup
    )


@router.callback_query(F.data.startswith("alert_husary"))
async def husary_main_alert(call: types.CallbackQuery):
    await quran_hasanxon_husaynxon_alert(
        call=call
    )


@router.callback_query(F.data.startswith("content_husary:"))
async def husary_main_content(call: types.CallbackQuery):
    await quran_hasanxon_husaynxon_content(
        call=call
    )
