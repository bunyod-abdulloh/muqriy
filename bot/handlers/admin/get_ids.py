from aiogram import Router, F, types

from loader import db

router = Router()


@router.message(F.video)
async def video_handler(message: types.Message):
    msg = message.caption_entities[0].url

    print(msg)

    # print(message.audio)
    # print(message.caption)
    # get_id = message.caption.split('|')[-1]
    # get_id_ = get_id.split('-')[0]
    # print(get_id_)

    # for n in range(27):
    #     await db.update_videos_qurantanishuv(
    #         video_id=message.video.file_id
    #     )
        # await db.add_audio_quranishuv(
        #     audio_id=message.audio.file_id, caption=message.caption, link=None
        # )
