from typing import AsyncIterator, cast, Optional
import asyncio
import zlib
from aiokafka import AIOKafkaConsumer
from manticore.components.sources.generic_source import GenericSource
from manticore.config.config import Config
from manticore.objects.generic_object import Package
from manticore.utils.logger import Logger


class KafkaSource(GenericSource):
    @staticmethod
    def get_type() -> str:
        return 'KafkaSource'

    def __init__(self, name: str, cfg: Config):
        super().__init__(name, cfg)
        self._broker_host = cfg.get(name, 'broker_host')
        self._auto_offset_reset = cfg.get(name, 'auto_offset_reset')
        self._max_poll_records = cfg.get(name, 'max_poll_records')
        self._enable_auto_commit = cfg.get(name, 'enable_auto_commit')
        self._compressed = cfg.get(name, 'compressed')
        self._kafka_consumer = cast(AIOKafkaConsumer, None)
        self._symbols = cfg.get(name, 'symbols')
        self._is_generator = True

        if not self._auto_offset_reset:
            raise RuntimeError('KafkaSource needs auto_offset_reset to be set (earliest/latest)')

        if not self._enable_auto_commit:
            Logger().info('enable_auto_commit is enabled')
            self._enable_auto_commit = True

        if self._max_poll_records:
            Logger().info('max_poll_records is NOT set')
            self._max_poll_records = int(self._max_poll_records)

        # self._last_seq_num_per_topic = {}

        # Initialise interface
        from manticore.components.sources.kafka_source.kafka_source_api import kafka_source_router
        from manticore.workers.generic_api import processor_api
        processor_api.include_router(kafka_source_router, prefix=f'/{self.name}', tags=[self.name])


    async def init(self) -> bool:
        self._kafka_consumer = AIOKafkaConsumer(loop=asyncio.get_event_loop(),
                                                bootstrap_servers=self._broker_host,
                                                auto_offset_reset=self._auto_offset_reset,
                                                max_poll_records=self._max_poll_records,
                                                enable_auto_commit=self._enable_auto_commit)
        self._kafka_consumer.subscribe(self._symbols)
        await self._kafka_consumer.start()

        self._valid = True
        return self._valid

    async def recv(self) -> AsyncIterator[Optional[Package]]:
        async for wire in self._kafka_consumer:
            msg = wire.value
            if self._compressed:
                msg = zlib.decompress(msg)

            pkg = self._decoder.decode(msg)

            # seq_num = obj.get_sequence_number()
            # if wire.topic in self._last_seq_num_per_topic and seq_num -
            # self._last_seq_num_per_topic[wire.topic] != 1:
            #     raise RuntimeError(f'Missed messages on {wire.topic}'
            #                        f'from {self._last_seq_num_per_topic[wire.topic]}
            # to {seq_num}')
            # self._last_seq_num_per_topic[wire.topic] = seq_num

            if not self._allowed_types or pkg.obj_type in self._allowed_types:
                yield pkg
            else:
                yield None
