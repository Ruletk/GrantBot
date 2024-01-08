from aiogram import Router

grant_router = Router(name="grant")


from .management import management_router
from .list import list_router
from .create import create_router

grant_router.include_routers(management_router, list_router, create_router)
