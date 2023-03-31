import asyncio
from manticore.components.sources.generic_source import GenericSource
from manticore.config.config import Config
from manticore.objects.generic_object import Package
from manticore.objects.objects_factory import ObjectsFactory
from manticore.objects.normalised.mock import MockV1, MockV2
from manticore.utils.logger import Logger
import manticore.utils.time_utils as tutil


class MockSource(GenericSource):
    @staticmethod
    def get_type() -> str:
        return 'MockSource'

    def __init__(self, name: str, cfg: Config):
        super().__init__(name, cfg)
        self.sleep_time = cfg.get(name, 'sleep_time')
        self._sequence_number = 0

        # Initialise interface
        from manticore.components.sources.mock_source.mock_source_api import mock_source_router
        from manticore.workers.generic_api import processor_api
        processor_api.include_router(mock_source_router, prefix=f'/{self.name}', tags=[self.name])

    async def init(self) -> bool:
        self._valid = True
        return self._valid

    async def recv(self) -> Package:
        if self.sleep_time:
            await asyncio.sleep(self.sleep_time)

        if self._sequence_number % 2:
            obj = MockV1.build('MOCK_ID_V1', tutil.now_us(), 'MockData')
        else:
            obj = MockV2.build('MOCK_ID_V2', tutil.now_us(), 'MockData', 'MockData2')

        pkg = ObjectsFactory.make_package(obj, 'MockSource', 'MockDestination')
        self._sequence_number += 1

        Logger().info(f'{self._name}: received {self._sequence_number} messages')
        return pkg
