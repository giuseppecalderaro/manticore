import zlib
import zmq
import zmq.asyncio
from manticore.components.sinks.generic_sink import GenericSink
from manticore.config.config import Config
from manticore.objects.generic_object import Package


class NetworkSink(GenericSink):
    @staticmethod
    def get_type() -> str:
        return 'NetworkSink'

    def __init__(self, name: str, cfg: Config):
        super().__init__(name, cfg)
        self._context = zmq.asyncio.Context()
        self._socket = self._context.socket(zmq.PUB)
        self._address = cfg.get(name, 'address')
        self._compressed = cfg.get(name, 'compressed')
        self._sent_objs = 0

        # Initialise interface
        from manticore.components.sinks.network_sink.network_sink_api import network_sink_router
        from manticore.workers.generic_api import processor_api
        processor_api.include_router(network_sink_router, prefix=f'/{self.name}', tags=[self.name])

    async def init(self) -> bool:
        self._socket.bind(self._address)
        return True

    async def send(self, item: Package) -> bool:
        wire, _ = self._encoder.encode(item)
        if self._compressed:
            wire = zlib.compress(wire)

        await self._socket.send(wire)
        self._sent_objs += 1
        return True
