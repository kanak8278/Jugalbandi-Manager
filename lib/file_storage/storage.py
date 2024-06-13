import os
import logging
from contextlib import asynccontextmanager
from abc import ABC, abstractmethod
import aiofiles
from aiofiles.threadpool.text import AsyncTextIOWrapper
from aiofiles.threadpool.binary import AsyncBufferedIOBase
from typing import AsyncGenerator, Union, Optional

logger = logging.getLogger(__name__)


class Storage(ABC):

    @abstractmethod
    async def write_file(
        self,
        file_path: str,
        file_content: Union[str, bytes],
        mime_type: Optional[str] = None,
    ):
        """
        Write external file to internal storage
        e.g. Channel service: storing a link from channel to storage account or docker volume
        """

    @asynccontextmanager
    async def read_file(
        self, file_path: Union[str, os.PathLike], mode="r"
    ) -> AsyncGenerator[Union[AsyncTextIOWrapper, AsyncBufferedIOBase], None]:
        """
        Read file from internal storage
        e.g. Langugage service: reading a file from storage account or docker volume

        with read_file(file_path) as file:
            # do something with the file

        """
        # download the file to the temporary directory
        temp_file_path: Union[str, os.PathLike] = (
            await self._download_file_to_temp_storage(file_path)
        )
        # read the file
        try:
            async with aiofiles.open(temp_file_path, mode) as file:
                yield file
        finally:
            await self._delete_temp_file(temp_file_path)

    @abstractmethod
    async def _download_file_to_temp_storage(
        self, file_path: Union[str, os.PathLike]
    ) -> Union[str, os.PathLike]:
        pass

    async def _delete_temp_file(self, file_path: Union[str, os.PathLike]):
        os.remove(file_path)

    @abstractmethod
    async def public_url(self, file_path: str) -> str:
        pass
