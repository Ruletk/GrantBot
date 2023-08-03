from aiohttp import ClientSession
from aiohttp import ContentTypeError

from src.api.exceptions import ServerError
from src.db.dals import UserDAL

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

        if response.status not in [200, 404]:
            details = await response.text()
            raise ServerError(f"Server returned {response.status}, details: {details}")
        try:
            data = await response.json()
        except ContentTypeError as e:
            print(e)
        return data, response.status

    async def get_grant_result(self, user_dal: UserDAL):
        iin, ikt, type, year = await user_dal.get_all_data()
        if not all([iin, ikt, type, year]):
            raise ValueError("Field should be filled")
        url = f"grant/test-type/{type}/test-year/{year}/student/{ikt}/iin/{iin}"
        return await self._make_request("GET", url)

    async def close_session(self):
        await self._http_client.close()
