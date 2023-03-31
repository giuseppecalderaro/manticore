from typing import Any, cast
import os
import aiofiles
from manticore.components.sinks.generic_sink import GenericSink
from manticore.config.config import Config
from manticore.objects.generic_object import Package
from manticore.utils.logger import Logger
from manticore.utils.time_utils import append_datetime


class FileSink(GenericSink):
    @staticmethod
    def get_type() -> str:
        return 'FileSink'

    def __init__(self, name: str, cfg: Config):
        super().__init__(name, cfg)
        self._file_path = cfg.get(name, 'file_path')
        self._mode = cfg.get(name, 'mode')
        self._fd: Any = None
        self._sent_objs = 0

        # Initialise interface
        from manticore.components.sinks.file_sink.file_sink_api import file_sink_router
        from manticore.workers.generic_api import processor_api
        processor_api.include_router(file_sink_router, prefix=f'/{self.name}', tags=[self.name])

    def __del__(self):
        if self._fd:
            self._fd.close()

    async def init(self) -> bool:
        if not self._encoder.is_compatible(self._mode):
            Logger().error(f'Encoder {self._encoder.name} does not support mode {self._mode}')
            return False

        self._file_path = append_datetime(self._file_path)
        self._fd = await aiofiles.open(self._file_path, 'wb' if self._mode == 'binary' else 'w')
        if not await self._fd.writable():
            Logger().error(f'{self._name}: Failed to open file: {self._file_path}')
            return False

        return True

    async def complete(self) -> bool:
        if self._flush_threshold != 0 and self._flush_threshold < self._sent_objs:
            await self._fd.flush()
            self._sent_objs = 0
            Logger().debug(f'{self._name}: Sent {self._sent_objs}')
            return True

        return False

    async def send(self, item: Package) -> bool:
        n_item, n_length = self._encoder.encode(item)
        data = cast(Any, None)

        if self._mode == 'binary':
            data = n_length.to_bytes(8, byteorder='little') + n_item
        else:
            data = n_item.decode('utf-8') + os.linesep

        await self._fd.write(data)
        await self._fd.flush()
        self._sent_objs += 1
        return True
