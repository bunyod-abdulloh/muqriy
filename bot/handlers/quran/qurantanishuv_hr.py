from aiogram import Router, F, types

router = Router()


@router.message(F.text == "Qur'on bilan tanishuv")
async def qurantanishuv_hr_main(message: types.Message):
    pass

