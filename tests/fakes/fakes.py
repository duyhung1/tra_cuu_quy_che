"""Test-only fakes. The AI fakes live in app/adapters/ai_fake.py and are re-exported here."""

import hashlib
import io
from typing import IO

from app.adapters.ai_fake import FakeEmbedder, FakeLLM, bag_of_words_vector

__all__ = ["FakeEmbedder", "FakeLLM", "FakeStorage", "FakeUpload", "bag_of_words_vector"]


class FakeStorage:
    def __init__(self) -> None:
        self.objects: dict[str, bytes] = {}

    async def put_stream(self, key: str, fileobj: IO[bytes]) -> str:
        data = fileobj.read()
        self.objects[key] = data
        return hashlib.sha256(data).hexdigest()

    async def get_bytes(self, key: str) -> bytes:
        return self.objects[key]

    async def delete(self, key: str) -> None:
        self.objects.pop(key, None)


class FakeUpload:
    """Mimics starlette UploadFile.read()."""

    def __init__(self, filename: str, data: bytes) -> None:
        self.filename = filename
        self._buf = io.BytesIO(data)

    async def read(self, size: int = -1) -> bytes:
        return self._buf.read(size)
