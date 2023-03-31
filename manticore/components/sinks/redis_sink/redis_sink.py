import zlib
import aioredis
from manticore.components.sinks.generic_sink import GenericSink
from manticore.config.config import Config
from manticore.objects.generic_object import Package
from manticore.utils.logger import Logger


class RedisSink(GenericSink):
    @staticmethod
    def get_type() -> str:
        return 'RedisSink'

    def __init__(self, name: str, cfg: Config):
        super().__init__(name, cfg)
        self._address = cfg.get(name, 'address')
        self._port = cfg.get(name, 'port')
        self._redis: aioredis.Redis = None
        self._compressed: bool = False
        self._sent_objs: int = 0

        # Initialise interface
        from manticore.components.sinks.redis_sink.redis_sink_api import redis_sink_router
        from manticore.workers.generic_api import processor_api
        processor_api.include_router(redis_sink_router, prefix=f'/{self.name}', tags=[self.name])

    async def init(self) -> bool:
        self._redis = await aioredis.from_url(f'redis://{self._address}:{self._port}')
        return True

    async def complete(self) -> bool:
        return False

    async def send(self, item: Package) -> bool:
        wire, _ = self._encoder.encode(item)
        if self._compressed:
            wire = zlib.compress(wire)

        await self._redis.publish(item.destination, wire)

        Logger().debug(f'''{self._name} sent an object {item.payload.get_id()} '''
                       f'''with header destination {item.destination}''')
        self._sent_objs += 1
        return True
