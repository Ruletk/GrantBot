from aiogram.dispatcher.router import Router


router = Router()


from .main_handlers import main_router
from .settings_handlers import settings_router
from .welcome_handlers import welcome_router
from .info_handlers import info_router


router.include_routers(main_router, settings_router, welcome_router, info_router)
