from typing import cast, Optional
import zlib
import zmq
import zmq.asyncio
from manticore.components.sources.generic_source import GenericSource
from manticore.config.config import Config
from manticore.objects.generic_object import Package
from manticore.utils.logger import Logger


class NetworkSource(GenericSource):
    @staticmethod
    def get_type() -> str:
        return 'NetworkSource'

    def __init__(self, name: str, cfg: Config):
        super().__init__(name, cfg)
        self._context = zmq.asyncio.Context()
        self._socket = self._context.socket(zmq.SUB)
        self._source_address = cfg.get(name, 'source_address')
        self._compressed = cfg.get(name, 'compressed')

        # Initialise interface
        from manticore.components.sources.network_source.network_source_api import network_source_router
        from manticore.workers.generic_api import processor_api
        processor_api.include_router(network_source_router, prefix=f'/{self.name}', tags=[self.name])

    async def init(self) -> bool:
        # timeout = 0
        # self._socket.setsockopt(zmq.RCVTIMEO, timeout)
        # Logger().info(f'Set receive timeout to {timeout}')

        hwm = 0
        self._socket.set_hwm(hwm)
        Logger().info(f'Set high watermark to {hwm}')

        # Subscribe to everything
        # self._socket.subscribe('')
        self._socket.setsockopt_string(zmq.SUBSCRIBE, '')

        self._socket.connect(self._source_address)

        self._valid = True
        return self._valid

    async def recv(self) -> Optional[Package]:
        ret = cast(Package, None)

        wire = await self._socket.recv()
        if not wire:
            return ret

        if self._compressed:
            wire = zlib.decompress(wire)

        pkg = self._decoder.decode(wire)
        if not self._allowed_types or pkg.obj_type in self._allowed_types:
            ret = pkg

        return ret
