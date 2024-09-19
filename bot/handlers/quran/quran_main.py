from aiogram import Router, F, types
from bot.keyboards.reply.user_main import quran_main_buttons

router = Router()


@router.message(F.text == "📖 Qur'oni Karim")
async def quran_main_handler(message: types.Message):
    await message.answer(
        text=message.text, reply_markup=quran_main_buttons()
    )
