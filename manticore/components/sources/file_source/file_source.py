from typing import cast, IO, Optional
import aiofiles
from manticore.components.sources.generic_source import GenericSource
from manticore.config.config import Config
from manticore.objects.generic_object import Package
from manticore.utils.logger import Logger


class FileSource(GenericSource):
    @staticmethod
    def get_type() -> str:
        return 'FileSource'

    def __init__(self, name: str, cfg: Config):
        super().__init__(name, cfg)
        self._file_path = cfg.get(name, 'file_path')
        self._mode = cfg.get(name, 'mode')
        self._fd = cast(IO, None)
        self._sequence_number = 0

        # Initialise interface
        from manticore.components.sources.file_source.file_source_api import file_source_router
        from manticore.workers.generic_api import processor_api
        processor_api.include_router(file_source_router, prefix=f'/{self.name}', tags=[self.name])

    def __del__(self):
        if self._fd:
            self._fd.close()

    @property
    def sequence_number(self):
        return self._sequence_number

    async def init(self) -> bool:
        if not self._decoder.is_compatible(self._mode):
            Logger().error(f'Decoder {self._decoder.name} does not support mode {self._mode}')
            return self._valid

        self._fd = await aiofiles.open(self._file_path, 'rb' if self._mode == 'binary' else 'r')
        self._valid = True
        return self._valid

    async def recv(self) -> Optional[Package]:
        ret = cast(Package, None)

        if self._mode == 'binary':
            length = await self._fd.read(8)
            if length == b'':  # EOF
                Logger().info(f'{self._name}: read {self._sequence_number} messages')
                self._valid = False
                return ret

            n_item = await self._fd.read(int.from_bytes(length, byteorder='little'))
        else:
            n_item = await self._fd.readline()
            if n_item == '':  # EOF
                Logger().info(f'{self._name}: read {self._sequence_number} messages')
                self._valid = False
                return ret
            n_item = n_item.encode('utf-8')

        pkg = self._decoder.decode(n_item)

        if not self._allowed_types or pkg.obj_type in self._allowed_types:
            ret = pkg

        self._sequence_number += 1
        return ret
