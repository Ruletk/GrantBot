import logging
from time import time

from aiogram.utils.i18n import lazy_gettext as _
from sqlalchemy import select

from src.api.requester import Api
from src.bot.text import Text
from src.db.models.Grant import Grant
from src.injector.injector import injector


logger = logging.getLogger(__name__)


class GrantDAO:
    def __init__(self, grant: Grant = None):
        logger.debug("Initializing")
        self.session = injector.get("session")
        self.grant: Grant = grant

    async def _get_grant(self, **kwargs) -> Grant | None:
        """Generalized method for getting grant by any field."""
        logger.debug("Getting grant, kwargs: %s", kwargs)
        async with self.session() as session:
            stmt = select(Grant).filter_by(**kwargs)
            res = await session.execute(stmt)
            self.grant = res.scalars().first()
            return self.grant

    async def _save_grant(self) -> None:
        logger.debug("Saving grant")
        async with self.session() as session:
            session.add(self.grant)
            await session.commit()

    async def _update_grant(self, **kwargs) -> None:
        logger.debug("Updating grant, kwargs: %s", kwargs)
        {setattr(self.grant, key, value) for key, value in kwargs.items()}  # noqa
        await self._save_grant()

    async def create_grant(self, grant: Grant) -> Grant | None:
        logger.debug("Creating grant: %s", grant)
        self.grant = grant
        await self._save_grant()
        return self.grant

    async def get_grant_by_ikt(self, ikt: str) -> Grant | None:
        """Find grant by ikt."""
        logger.debug("Getting grant by ikt: %s", ikt)
        return await self._get_grant(ikt=ikt, is_active=1)

    async def get_cached(self) -> dict:
        logger.debug("Getting cached grant")
        if (
            self.grant.last_request
            and self.grant.last_request.get("last_time") - time() < 60 * 30
        ):
            return self.grant.last_request
        return await self._cache()

    async def _cache(self) -> dict:
        """Caching grant result from api to database."""
        logger.debug("Caching grant")
        async with Api() as api:
            try:
                logger.debug("Sending response to api, api: %s", api)
                data = await api.get_grant_result(self.grant)

                if data.get("data", {}).get("hasGrant"):
                    data["data"] |= {"url": await api.get_download_url(self.grant)}

                self.grant.last_request = {"last_time": time()} | data
                logger.debug("Caching and saving grant, data: %s", data)

                await self._save_grant()
                return self.grant.last_request
            except ValueError:
                logger.debug("Caching grant failed")
                return {"errorCode": 1, "errorMessage": "Field should be filled"}

    async def get_result(self):
        logger.debug("Getting grant result")
        data = await self.get_cached()
        if data.get("data", {}).get("hasGrant"):
            return data.get("data", {}) | {"error_code": 0}
        return data

    async def get_type(self):
        return _([Text.ent, Text.mag, Text.nkt][self.grant.type - 1])

    async def get_ikt(self):
        return self.grant.ikt

    async def delete_grant(self):
        logger.info("Deleting grant: %s", self.grant)
        self.grant.is_active = 0
        self.grant.last_request = None
        await self._save_grant()
