from aiohttp import ClientSession
from typing import AsyncGenerator

class APIClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(APIClient, cls).__new__(cls, *args, **kwargs)
            cls._instance.session = ClientSession()
        return cls._instance

    async def cleanup(self):
        await self.session.close()

    async def post_request(self, url, headers, payload):
        async with self.session.post(url, headers=headers, json=payload) as resp:
            if resp.status != 200:
                server_resp = await resp.text()
                raise Exception(f"Error in API: {server_resp}")
            return await resp.json()

    async def get_request(self, url, headers):
        async with self.session.get(url, headers=headers) as resp:
            if resp.status != 200:
                raise Exception(f"Error in API: {resp.status}")
            return await resp.json()
        
    async def download(self, url) -> AsyncGenerator[bytes, None]:
        async with self.session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"Error in API: {resp.status}")
            async for chunk in resp.content.iter_chunked(1024):
                yield chunk
        
