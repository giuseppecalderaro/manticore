from typing import Any, AsyncIterator, Optional
import zlib
import aioredis
from manticore.components.sources.generic_source import GenericSource
from manticore.config.config import Config
from manticore.objects.generic_object import Package
from manticore.utils.logger import Logger


class RedisSource(GenericSource):
    @staticmethod
    def get_type() -> str:
        return 'RedisSource'

    def __init__(self, name: str, cfg: Config):
        super().__init__(name, cfg)
        self._is_generator = True
        self._address = cfg.get(name, 'address')
        self._port = cfg.get(name, 'port')
        self._symbols = cfg.get(name, 'symbols')
        self._compressed = False
        self._sequence_number = 0

        self._redis: Any = None
        self._receiver: Any = None

        # Initialise interface
        from manticore.components.sources.redis_source.redis_source_api import redis_source_router
        from manticore.workers.generic_api import processor_api
        processor_api.include_router(redis_source_router, prefix=f'/{self.name}', tags=[self.name])

    async def init(self) -> bool:
        self._redis = await aioredis.from_url(f'redis://{self._address}:{self._port}')
        self._receiver = self._redis.pubsub()

        for symbol in self._symbols:
            await self._receiver.subscribe(symbol)

        Logger().info('RedisSource initialised')

        self._valid = True
        return self._valid

    async def recv(self) -> AsyncIterator[Optional[Package]]:
        async for msg in self._receiver.listen():
            msg_type = msg.get('type', None)

            if msg_type == 'message':
                msg_data = msg.get('data', None)

                if msg_data:
                    if self._compressed:
                        msg_data = zlib.decompress(msg_data)

                pkg = self._decoder.decode(msg_data)

                if not self._allowed_types or pkg.obj_type in self._allowed_types:
                    self._sequence_number += 1
                    Logger().debug(f'{self._name}: received {self._sequence_number} messages')
                    yield pkg
                else:
                    yield None
