from aiohttp import ClientSession
from aiohttp import ContentTypeError

from src.db.dals import UserDAL

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

    async def get_grant_result(self, user_dal: UserDAL):
        iin, ikt, type, year = await user_dal.get_all_data()
        if not all([iin, ikt, type, year]):
            raise ValueError("Field should be filled")
        url = f"{API_BASE_URL}/grant/test-type/{type}/test-year/{year}/student/{ikt}/iin/{iin}"
        return await self._make_request("GET", url)

    async def get_download_url(self, user_dal: UserDAL):
        iin, ikt, type, year = await user_dal.get_all_data()
        url = (
            f"{API_BASE_DOWNLOAD_URL}/grant/download-link/test-type"
            f"/{type}/year/{year}/student/{ikt}/iin/{iin}"
        )
        data = await self._make_request("GET", url)

        download_url = data.get("data").get("certificateDownLoadUrl")
        return download_url

    async def close_session(self):
        await self._http_client.close()
