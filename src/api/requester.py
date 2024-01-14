import logging

from aiohttp import ClientSession
from aiohttp import ContentTypeError

from src.db.models.Grant import Grant

API_BASE_URL = "https://grant.testcenter.kz/certificate/api/v1"
API_BASE_DOWNLOAD_URL = "https://grant.testcenter.kz/api/v1/certificate"

logger = logging.getLogger(__name__)


class Api:
    def __init__(self):
        self._http_client = ClientSession()

    def __str__(self):
        return f"<Api(http_client={self._http_client})>"

    async def __aenter__(self):
        self._http_client = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_session()

    async def close_session(self):
        if self._http_client:
            await self._http_client.close()
            self._http_client = None

    async def _make_request(self, method, url) -> dict | None:
        """Make request to api and return json or None""" ""
        try:
            response = await self._http_client.request(method=method, url=url)
            data = await response.json()
            return data
        except ContentTypeError as e:
            logger.exception(e)
            return None
        except Exception as e:
            logger.exception(e)

    async def get_grant_result(self, grant: Grant) -> dict | None:
        """Make request to grant api and return json or None"""
        if not any([grant.iin, grant.ikt, grant.type, grant.year]):
            raise ValueError("Field should be filled")
        url = (
            f"{API_BASE_URL}/grant"
            f"/test-type/{grant.type}"
            f"/test-year/{grant.year}"
            f"/student/{grant.ikt}"
            f"/iin/{grant.iin}"
        )
        data = await self._make_request("GET", url)
        return data

    async def get_download_url(self, grant: Grant) -> str:
        """Return download url for certificate
        or empty string if certificate not found."""
        url = (
            f"{API_BASE_DOWNLOAD_URL}/grant/download-link/"
            f"test-type/{grant.type}"
            f"/year/{grant.year}"
            f"/student/{grant.ikt}"
            f"/iin/{grant.iin}"
        )
        data = await self._make_request("GET", url) or {}

        download_url = data.get("data", {}).get("certificateDownLoadUrl", "")
        return download_url
