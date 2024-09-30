from aiogram import Router, F, types

from bot.keyboards.inline.general_ibuttons import audio_video_ibuttons, back_ibutton
from bot.keyboards.inline.qurantanishuv_ibuttons import qurantanishuv_buttons
from loader import db

router = Router()

text = ("Ulamolarimiz, xususan, ustozimiz Shayx Muhammad Sodiq Muhammad Yusuf rahmatullohi alayhi har yili Ramazon "
        "oyida o‘ziga xos tayyorgarlik qilib, ushbu oyda xalqimizga nimadir yangi bir yoki bir necha ilmiy tuhfa "
        "taqdim etardilar. Ulug‘larimizning an’analarini davom ettirishga xizmat qilish ilinjida aynan Shayx "
        "hazratlari nomidagi masjidda 1442 - hijriy yil Ramazon oyi uchun yangi ilmiy suhbatlar turkumi taqdim "
        "etildi. Ushbu suhbatlar 26 ta suhbatlar turkumidan iborat. Bunda har kuni oqshom tarovehda o‘qiladigan sura "
        "va oyatlar bilan tanishib borilgan. Alloh O‘zi maqbul va manzur etsin! Duolaringizdan umidvormiz!")


@router.message(F.text == "Qur'on bilan tanishuv")
async def qurantanishuv_hr_main(message: types.Message):
    await message.answer(
        text=text, reply_markup=audio_video_ibuttons(
            callback="qurantanishuv"
        )
    )


@router.callback_query(F.data == "qurantanishuv_back")
async def qurantanishuv_back_rtr(call: types.CallbackQuery):
    await call.message.edit_text(
        text=text, reply_markup=audio_video_ibuttons(
            callback="qurantanishuv"
        )
    )


@router.callback_query(F.data == "audio:qurantanishuv")
async def qurantanishuv_audio_rtr(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Suhbatlardan birini tanlang", reply_markup=qurantanishuv_buttons(
            callback="qurantanishuvaudio"
        )
    )


@router.callback_query(F.data.startswith("qurantanishuvaudio"))
async def qurantanishuv_get_audio(call: types.CallbackQuery):
    await call.answer(
        cache_time=0
    )
    id_ = call.data.split(':')[1]
    datas = await db.select_file_qurantanishuv(
        id_=id_
    )
    audio = datas['audio_id']
    caption = datas['caption']

    await call.message.answer_audio(
        audio=audio, caption=caption, reply_markup=back_ibutton(
            callback="audio_qurantanishuvmain"
        )
    )


@router.callback_query(F.data == "audio_qurantanishuvmain")
async def qurantanishuv_main_audio(call: types.CallbackQuery):
    await call.answer(
        cache_time=0
    )
    await call.message.answer(
        text="Suhbatlardan birini tanlang", reply_markup=qurantanishuv_buttons(
            callback="qurantanishuvaudio"
        )
    )


@router.callback_query(F.data == "video:qurantanishuv")
async def qurantanishuv_video_rtr(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Suhbatlardan birini tanlang", reply_markup=qurantanishuv_buttons(
            callback="qurantanishuvvideo"
        )
    )


@router.callback_query(F.data.startswith("qurantanishuvvideo"))
async def qurantanishuv_get_audio(call: types.CallbackQuery):
    await call.answer(
        cache_time=0
    )
    id_ = call.data.split(':')[1]
    datas = await db.select_file_qurantanishuv(
        id_=id_
    )
    video = datas['video_id']
    caption = datas['caption']

    await call.message.answer_video(
        video=video, caption=caption, reply_markup=back_ibutton(
            callback="video_qurantanishuvmain"
        )
    )


@router.callback_query(F.data == "video_qurantanishuvmain")
async def qurantanishuv_main_audio(call: types.CallbackQuery):
    await call.answer(
        cache_time=0
    )
    await call.message.answer(
        text="Suhbatlardan birini tanlang", reply_markup=qurantanishuv_buttons(
            callback="qurantanishuvvideo"
        )
    )
