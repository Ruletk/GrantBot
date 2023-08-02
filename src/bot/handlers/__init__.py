from aiogram.dispatcher.router import Router


router = Router()


from .main_handlers import main_router
from .settings_handlers import settings_router
from .welcome_handlers import welcome_router

router.include_router(main_router)
router.include_router(settings_router)
router.include_router(welcome_router)
