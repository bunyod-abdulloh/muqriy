from aiogram import Router

from bot.filters import ChatPrivateFilter


def setup_routers() -> Router:
    from .admin import get_ids
    from .users import admin, start
    from bot.handlers.quran import qurantanishuv_hr, muqriyrecitation_hr, husarymain_hr, husaryselect_hr, quran_main
    from .errors import error_handler

    router = Router()

    # Agar kerak bo'lsa, o'z filteringizni o'rnating
    start.router.message.filter(ChatPrivateFilter(chat_type=["private"]))
    # Users
    router.include_routers(
        start.router, muqriyrecitation_hr.router, husarymain_hr.router, husaryselect_hr.router,
        quran_main.router, qurantanishuv_hr.router
    )
    # Admin
    router.include_routers(
        admin.router, error_handler.router, get_ids.router)

    return router
