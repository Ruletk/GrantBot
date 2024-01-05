from aiohttp import ClientSession
from aiohttp import ContentTypeError

from src.db.dao.UserDAO import UserDAO

API_BASE_URL = "https://grant.testcenter.kz/certificate/api/v1"
API_BASE_DOWNLOAD_URL = "https://grant.testcenter.kz/api/v1/certificate"


class Api:
    def __init__(self):
        self._http_client = ClientSession()

    async def _make_request(self, method, url):
        try:
            response = await self._http_client.request(method=method, url=url)
        except Exception as e:
            print(e)

        try:
            data = await response.json()
        except ContentTypeError as e:
            print(e)
        return data

    async def get_grant_result(self, user_dal: UserDAO):
        data = user_dal.user.to_json()
        if (
            not data.get("iin")
            or not data.get("ikt")
            or not data.get("type")
            or not data.get("year")
        ):
            raise ValueError("Field should be filled")
        url = (
            f"{API_BASE_URL}/grant"
            f"/test-type/{data.get('type')}"
            f"/test-year/{data.get('year')}"
            f"/student/{data.get('ikt')}"
            f"/iin/{data.get('iin')}"
        )
        return await self._make_request("GET", url)

    async def get_download_url(self, user_dal: UserDAO):
        data = user_dal.user.to_json()
        url = (
            f"{API_BASE_DOWNLOAD_URL}/grant/download-link/"
            f"test-type/{data.get('type')}"
            f"/year/{data.get('year')}"
            f"/student/{data.get('ikt')}"
            f"/iin/{data.get('iin')}"
        )
        data = await self._make_request("GET", url)

        download_url = data.get("data").get("certificateDownLoadUrl")
        return download_url

    async def close_session(self):
        await self._http_client.close()
