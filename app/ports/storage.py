from typing import IO, Protocol


class ObjectStoragePort(Protocol):
    async def put_stream(self, key: str, fileobj: IO[bytes]) -> str:
        """Store the file object and return its sha256 hex digest."""
        ...

    async def get_bytes(self, key: str) -> bytes: ...

    async def delete(self, key: str) -> None: ...
