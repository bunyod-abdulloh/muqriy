from pprint import pprint

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

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
async def husary_first_rtr(message: types.Message):
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


@router.callback_query(F.data.startswith("select_husary:"))
async def husary_select_rtr(call: types.CallbackQuery, state: FSMContext):
    sura_number = call.data.split(":")[1]

    sura = await db.select_husary(
        sequence=sura_number
    )

    # await call.message.answer_audio(
    #     audio=sura['audiohusary']
    # )
    # await call.message.answer_document(
    #     document=sura['zip']
    # )

    await call.message.answer(
        text=f"Sura nomi: {sura['sura_name']}\n"
             f"Oyatlar soni: {sura['total_verses']}\n"
             f"Oyat tartib raqamini kiriting:"
    )
    await state.update_data(
        sura_number=sura_number
    )
    await state.set_state(Husary.get_ayah)


@router.message(Husary.get_ayah)
async def husary_ayah_rtr(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sura_number = data['sura_number'].lstrip('0')
    ayah_number = int(message.text)


    sura = await db.select_husary_verses(
        sequence=data['sura_number']
    )
    if message.text.isdigit() and ayah_number <= sura['total_verses']:
        photo = f"https://www.everyayah.com/data/images_png/{sura_number}_{ayah_number}.png"
        audio = f"https://www.everyayah.com/data/Husary_Muallim_128kbps/{data['sura_number']}{ayah_number}.mp3"
        await message.answer_photo(
            photo=photo
        )
        if ayah_number == 1:
            await message.answer_audio(
                audio=audio, reply_markup=quran_next_ibutton(
                    sura_number=sura_number, ayah_number=ayah_number
                )
            )
        elif ayah_number == sura['total_verses']:
            await message.answer_audio(
                audio=audio, reply_markup=quran_prev_ibutton(
                    sura_number=sura_number, ayah_number=ayah_number
                )
            )
        else:
            await message.answer_audio(
                audio=audio, reply_markup=quran_next_prev_ibuttons(
                    sura_number=sura_number, ayah_number=ayah_number
                )
            )
    else:
        await message.answer(
            text=f"Oyat tartib raqami noto'g'ri kiritildi!\n\n"
                 f"{sura['sura_name']} surasidagi jami oyatlar soni {sura['total_verses']} ta"
        )
