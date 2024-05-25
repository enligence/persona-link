"""
Azure storage for cache
"""

import os
from typing import AsyncGenerator
from persona_link.cache.storage.base_storage import BaseCacheStorage
from azure.storage.blob.aio import BlobServiceClient, BlobClient
from azure.storage.blob import generate_blob_sas, BlobSasPermissions, ContentSettings
from azure.core.exceptions import ResourceNotFoundError
from datetime import datetime, timedelta, UTC

from persona_link.cache.models import ContentType

class AzureStorage(BaseCacheStorage):
    """
    Azure storage for cache.
    Requires ENV vars to be set for connection string and container name
    """

    def _getUrl(self, blob_client: BlobClient) -> str:
        # get temporary url to the resource that is publicly accessible for streaming
        expiry = datetime.now(UTC) + timedelta(hours=1)
        sas_token = generate_blob_sas(
            blob_client.account_name,
            blob_client.container_name,
            blob_client.blob_name,
            account_key=blob_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=expiry,
        )

        blob_sas_url = f"{blob_client.url}?{sas_token}"
        return blob_sas_url

    def __init__(self):
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

        if self.connection_string is None:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING must be set in ENV")
        if self.container_name is None:
            raise ValueError("AZURE_STORAGE_CONTAINER_NAME must be set in ENV")

    async def put(self, avatarId: str, data: bytes | AsyncGenerator[bytes, None], filename: str, content_type: ContentType) -> str:
        path = f"{avatarId}/{filename}"
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

        async with blob_service_client:
            container_client = blob_service_client.get_container_client(self.container_name)
            await container_client.upload_blob(path, data, overwrite=True, content_settings=ContentSettings(content_type=content_type))
        return path
    
    async def get(self, path: str) -> str:
        # get temporary url to the resource that is publicly accessible for streaming
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

        async with blob_service_client:
            container_client = blob_service_client.get_container_client(self.container_name)
            blob_client = container_client.get_blob_client(path)

            return self._getUrl(blob_client)

    async def delete(self, path: str) -> None:
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        async with blob_service_client:
            container_client = blob_service_client.get_container_client(self.container_name)
            try:
                blob_client = container_client.get_blob_client(path)
            except ResourceNotFoundError:
                return
            
            await blob_client.delete_blob()

    async def deleteAll(self, avatarId: str) -> None:
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        async with blob_service_client:
            container_client = blob_service_client.get_container_client(self.container_name)
            blobs = container_client.list_blobs(name_starts_with=avatarId)
            async for blob in blobs:
                await container_client.delete_blob(blob.name)