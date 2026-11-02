"""Object storage port + S3 adapter (S3Mock locally). boto3 is synchronous, so calls are
offloaded to a thread."""

import asyncio
import hashlib
from typing import IO, Protocol

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from app.platform.config import Settings, get_settings
from app.platform.errors import AppError


class ObjectStoragePort(Protocol):
    async def put_stream(self, key: str, fileobj: IO[bytes]) -> str: ...
    async def get_bytes(self, key: str) -> bytes: ...
    async def delete(self, key: str) -> None: ...


class S3Storage:
    def __init__(self, settings: Settings | None = None) -> None:
        s = settings or get_settings()
        self.bucket = s.s3_bucket
        self.use_kms = s.s3_use_kms
        self._client = boto3.client(
            "s3",
            endpoint_url=s.s3_endpoint_url,
            region_name=s.s3_region,
            config=Config(signature_version="s3v4", retries={"max_attempts": 3}),
        )

    def _extra_args(self) -> dict:
        return {"ServerSideEncryption": "aws:kms"} if self.use_kms else {}

    async def put_stream(self, key: str, fileobj: IO[bytes]) -> str:
        """Upload a file object and return its sha256 hex digest."""

        def _upload() -> str:
            digest = hashlib.sha256()
            fileobj.seek(0)
            for block in iter(lambda: fileobj.read(1024 * 1024), b""):
                digest.update(block)
            fileobj.seek(0)
            self._client.upload_fileobj(
                fileobj, self.bucket, key, ExtraArgs=self._extra_args() or None
            )
            return digest.hexdigest()

        try:
            return await asyncio.to_thread(_upload)
        except (ClientError, BotoCoreError) as exc:
            raise AppError("storage_error", str(exc)) from exc

    async def get_bytes(self, key: str) -> bytes:
        def _get() -> bytes:
            return self._client.get_object(Bucket=self.bucket, Key=key)["Body"].read()

        try:
            return await asyncio.to_thread(_get)
        except (ClientError, BotoCoreError) as exc:
            raise AppError("storage_error", str(exc)) from exc

    async def delete(self, key: str) -> None:
        try:
            await asyncio.to_thread(self._client.delete_object, Bucket=self.bucket, Key=key)
        except (ClientError, BotoCoreError) as exc:
            raise AppError("storage_error", str(exc)) from exc
