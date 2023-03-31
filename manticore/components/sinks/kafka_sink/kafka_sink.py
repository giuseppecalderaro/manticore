from typing import Any
import asyncio
import zlib
import aiokafka
from manticore.components.sinks.generic_sink import GenericSink
from manticore.config.config import Config
from manticore.objects.generic_object import Package
from manticore.utils.logger import Logger


class KafkaSink(GenericSink):
    @staticmethod
    def get_type() -> str:
        return 'KafkaSink'

    def __init__(self, name: str, cfg: Config):
        super().__init__(name, cfg)
        self._broker_host = cfg.get(name, 'broker_host')
        self._compressed = cfg.get(name, 'compressed')
        self._kafka_producer: Any = None
        self._sent_objs = 0

        # Initialise interface
        from manticore.components.sinks.kafka_sink.kafka_sink_api import kafka_sink_router
        from manticore.workers.generic_api import processor_api
        processor_api.include_router(kafka_sink_router, prefix=f'/{self.name}', tags=[self.name])

    async def init(self) -> bool:
        self._kafka_producer = aiokafka.AIOKafkaProducer(loop=asyncio.get_event_loop(),
                                                         bootstrap_servers=self._broker_host)
        await self._kafka_producer.start()
        return True

    async def complete(self) -> bool:
        if self._flush_threshold != 0 and self._flush_threshold < self._sent_objs:
            await self._kafka_producer.flush()
            self._sent_objs = 0
            Logger().debug(f'{self._name}: Sent {self._sent_objs}')
            return True

        return False

    async def send(self, item: Package) -> bool:
        wire, _ = self._encoder.encode(item)
        if self._compressed:
            wire = zlib.compress(wire)

        await self._kafka_producer.send(item.destination, wire)
        self._sent_objs += 1
        return True
