from aiogram import Router, F

from loader import db
from utils.dicts.dicts import husary_dict

router = Router()


@router.message(F.text == "husary")
async def husary_handler(message):
    """
    Husary Ta'lim uslubida bo'limi bilan bog'liq sura va oyatlar ro'yxatini qo'shish uchun handler.'
    Args:
        message:

    Returns:

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
