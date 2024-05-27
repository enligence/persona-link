from aiohttp import ClientSession
from typing import AsyncGenerator

class APIClient:
    """
    Singleton class for the API Client to make api requests using async functions
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(APIClient, cls).__new__(cls, *args, **kwargs)
            cls._instance.session = ClientSession()
        return cls._instance

    async def cleanup(self):
        await self.session.close()

    async def post_request(self, url, headers=None, payload=None, response_format="json") -> dict:
        """
        Make a POST request to the given URL with the given headers and payload
        
        Parameters:
            url (str): The URL to make the request to
            headers (dict): The headers to send with the request
            payload (dict): The payload to send with the request
            response_format (str): The format of the response. Default is "json"
            
        Returns:
            The response of the request as json
        """
        async with self.session.post(url, headers=headers, json=payload) as resp:
            if resp.status >= 400:
                server_resp = await resp.text()
                raise Exception(f"Error in API: {server_resp}")
            return await resp.json() if response_format == "json" else await resp.text()
        
    async def put_request(self, url, headers=None, payload=None) -> dict:
        """
        Make a PUT request to the given URL with the given headers and payload
        
        Parameters:
            url (str): The URL to make the request to
            headers (dict): The headers to send with the request
            payload (dict): The payload to send with the request
            
        Returns:
            The response of the request as json
        """
        async with self.session.put(url, headers=headers, json=payload) as resp:
            if resp.status >= 400:
                server_resp = await resp.text()
                raise Exception(f"Error in API: {server_resp}")
            return await resp.json()

    async def get_request(self, url, headers=None) -> dict:
        """
        Make a GET request to the given URL with the given headers
        
        Parameters:
            url (str): The URL to make the request to
            headers (dict): The headers to send with the request
            
        Returns:
            The response of the request as json
        """
        async with self.session.get(url, headers=headers) as resp:
            if resp.status >= 400:
                raise Exception(f"Error in API: {resp.status}")
            return await resp.json()
        
    async def download(self, url) -> AsyncGenerator[bytes, None]:
        """
        Download the content from the given URL
        
        Parameters:
            url (str): The URL to download the content from
            
        Returns:
            The content of the response as async stream of bytes
        """
        async with self.session.get(url) as resp:
            if resp.status >= 400:
                raise Exception(f"Error in API: {resp.status}")
            async for chunk in resp.content.iter_chunked(1024):
                yield chunk
        
