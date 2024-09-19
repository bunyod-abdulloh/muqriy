from aiogram import Router, F, types

from loader import db

router = Router()


@router.message(F.text == "GEt id")
async def video_handler(message: types.Message):
    pass
