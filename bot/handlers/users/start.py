from aiogram import Router, types
from aiogram.filters import CommandStart

from bot.keyboards.reply.user_main import main_menu_buttons
from loader import db

router = Router()


@router.message(CommandStart())
async def do_start(message: types.Message):
    telegram_id = message.from_user.id
    try:
        await db.add_user(
            telegram_id=telegram_id)
    except Exception:
        pass
    await message.answer(
        text=f"Assalomu alaykum!",
        reply_markup=main_menu_buttons()
    )


@router.callback_query(F.data == "back_main")
async def back_to_main(call: types.CallbackQuery):
    await call.message.answer(
        text="Bosh sahifa",  reply_markup=main_menu_buttons()
    )
