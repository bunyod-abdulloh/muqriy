from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline.quran_ibuttons import quran_next_ibutton, quran_prev_ibutton, quran_next_prev_ibuttons
from bot.states.user_states import Husary
from loader import db

router = Router()


@router.callback_query(F.data.startswith("select_husary:"))
async def husary_select_rtr(call: types.CallbackQuery, state: FSMContext):
    await call.answer(
        cache_time=0
    )
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
    if message.text.isdigit():
        data = await state.get_data()
        sura_photo = data['sura_number'].lstrip('0')
        sura_audio = data['sura_number']
        ayah_photo = int(message.text)

        sura = await db.select_husary_verses(
            sequence=sura_audio
        )
        total_verses = sura['total_verses']

        if ayah_photo <= total_verses:

            ayah_audio = message.text.zfill(3)

            photo = f"https://www.everyayah.com/data/images_png/{sura_photo}_{ayah_photo}.png"
            audio = f"https://www.everyayah.com/data/Husary_Muallim_128kbps/{sura_audio}{ayah_audio}.mp3"

            await message.answer_photo(
                photo=photo
            )

            if ayah_photo == 1:
                await message.answer_audio(
                    audio=audio, reply_markup=quran_next_ibutton(
                        sura_audio=sura_audio, sura_photo=sura_photo, ayah_audio=message.text,
                        ayah_photo=ayah_photo, total_verses=total_verses
                    )
                )
            elif ayah_photo == total_verses:
                await message.answer_audio(
                    audio=audio, reply_markup=quran_prev_ibutton(
                        sura_audio=sura_audio, sura_photo=sura_photo, ayah_audio=message.text,
                        ayah_photo=ayah_photo, total_verses=total_verses
                    )
                )
            else:
                await message.answer_audio(
                    audio=audio, reply_markup=quran_next_prev_ibuttons(
                        sura_audio=sura_audio, sura_photo=sura_photo, ayah_audio=message.text,
                        ayah_photo=ayah_photo, total_verses=total_verses
                    )
                )
        else:
            await message.answer(
                text=f"Oyat tartib raqami noto'g'ri kiritildi!\n\n"
                     f"{sura['sura_name']} surasidagi jami oyatlar soni {total_verses} ta"
            )
    # else:
    #     await state.clear()


@router.callback_query(F.data.startswith('husarynext_'))
async def husary_ayah_fnext_rtr(call: types.CallbackQuery):
    await call.answer(
        cache_time=0
    )
    sura_audio = call.data.split('_')[1]
    sura_photo = call.data.split('_')[2]
    ayah_audio = int(call.data.split('_')[3]) + 1
    ayah_audio_ = str(ayah_audio).zfill(3)
    ayah_photo = int(call.data.split('_')[4]) + 1
    total_verses = int(call.data.split('_')[5])

    photo = f"https://www.everyayah.com/data/images_png/{sura_photo}_{ayah_photo}.png"
    audio = f"https://www.everyayah.com/data/Husary_Muallim_128kbps/{sura_audio}{ayah_audio_}.mp3"

    await call.message.answer_photo(
        photo=photo
    )

    if ayah_photo == total_verses:
        await call.message.answer_audio(
            audio=audio, reply_markup=quran_prev_ibutton(
                sura_audio=sura_audio, sura_photo=sura_photo, ayah_audio=ayah_audio,
                ayah_photo=ayah_photo, total_verses=total_verses
            )
        )
    else:
        await call.message.answer_audio(
            audio=audio, reply_markup=quran_next_prev_ibuttons(
                sura_audio=sura_audio, sura_photo=sura_photo, ayah_audio=ayah_audio,
                ayah_photo=ayah_photo, total_verses=total_verses
            )
        )


@router.callback_query(F.data.startswith('husaryprev_'))
async def husary_ayah_fprev_rtr(call: types.CallbackQuery):
    await call.answer(
        cache_time=0
    )
    sura_audio = call.data.split('_')[1]
    sura_photo = call.data.split('_')[2]
    ayah_audio = int(call.data.split('_')[3]) - 1
    ayah_audio_ = str(ayah_audio).zfill(3)
    ayah_photo = int(call.data.split('_')[4]) - 1
    total_verses = call.data.split('_')[5]

    photo = f"https://www.everyayah.com/data/images_png/{sura_photo}_{ayah_photo}.png"
    audio = f"https://www.everyayah.com/data/Husary_Muallim_128kbps/{sura_audio}{ayah_audio_}.mp3"

    await call.message.answer_photo(
        photo=photo
    )

    if str(ayah_photo) == '1':
        await call.message.answer_audio(
            audio=audio, reply_markup=quran_next_ibutton(
                sura_audio=sura_audio, sura_photo=sura_photo, ayah_audio=ayah_audio,
                ayah_photo=ayah_photo, total_verses=total_verses
            )
        )
    else:
        await call.message.answer_audio(
            audio=audio, reply_markup=quran_next_prev_ibuttons(
                sura_audio=sura_audio, sura_photo=sura_photo, ayah_audio=ayah_audio,
                ayah_photo=ayah_photo, total_verses=total_verses
            )
        )
