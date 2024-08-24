from typing import List

from aiogram import F, Router
from aiogram.types import (
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    Message
)

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
            pass
            # sura_number = element.audio.file_name.split(".")[0]
            # await message.answer(
            #     text=f"<code>{element.audio.file_id}</code>\n\n{element.audio.file_name}"
            # )
            # await db.update_edu_to_muqriy(
            #     sequence=sura_number,
            #     audiomuqriy=element.audio.file_id
            # )
        else:
            return message.answer("This media type isn't supported!")
