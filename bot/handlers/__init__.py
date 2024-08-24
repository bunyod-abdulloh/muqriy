from aiogram import Router

from bot.filters import ChatPrivateFilter


def setup_routers() -> Router:
    from .users import admin, start, husarymuallim_hr, muqriyrecitation_hr, quran_main
    from .errors import error_handler

    router = Router()

    # Agar kerak bo'lsa, o'z filteringizni o'rnating
    start.router.message.filter(ChatPrivateFilter(chat_type=["private"]))
    # Users
    router.include_routers(
        start.router, husarymuallim_hr.router, muqriyrecitation_hr.router, quran_main.router
    )
    # Admin
    router.include_routers(
        admin.router, error_handler.router)

    return router
