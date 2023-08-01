from aiohttp import ClientSession
from aiohttp import ContentTypeError
from aiohttp.web_exceptions import HTTPNotFound

from src.api.exceptions import ServerError
from src.db.models import User

API_BASE_URL = "https://grant.testcenter.kz/certificate/api/v1"


class Api:
    def __init__(self):
        self._http_client = ClientSession()

    async def _make_request(self, method, url_part):
        try:
            response = await self._http_client.request(
                method=method, url=f"{API_BASE_URL}/{url_part}"
            )
        except Exception as e:
            print(e)

        if response.status == 404:
            raise HTTPNotFound()

        if response.status != 200:
            details = await response.text()
            raise ServerError(f"Server returned {response.status}, details: {details}")
        try:
            data = await response.json()
        except ContentTypeError as e:
            print(e)
        return data

    async def get_grant_result(self, user: User):
        if not user or not all([user.iin, user.ikt, user.year, user.type]):
            raise ValueError("Field should be filled")
        url = f"grant/test-type/{user.type}/test-year/{user.year}/student/{user.ikt}/iin/{user.iin}"
        return await self._make_request("GET", url)

    async def close_session(self):
        await self._http_client.close()
