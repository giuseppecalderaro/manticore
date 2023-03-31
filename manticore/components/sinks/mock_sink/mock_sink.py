from manticore.components.sinks.generic_sink import GenericSink
from manticore.config.config import Config
from manticore.objects.generic_object import Package
from manticore.utils.logger import Logger


class MockSink(GenericSink):
    @staticmethod
    def get_type() -> str:
        return 'MockSink'

    def __init__(self, name: str, cfg: Config):
        super().__init__(name, cfg)
        self._sent_objs = 0

        # Initialise interface
        from manticore.components.sinks.mock_sink.mock_sink_api import mock_sink_router
        from manticore.workers.generic_api import processor_api
        processor_api.include_router(mock_sink_router, prefix=f'/{self.name}', tags=[self.name])

    async def init(self) -> bool:
        return True

    async def complete(self) -> bool:
        if self._flush_threshold != 0 and self._flush_threshold < self._sent_objs:
            self._sent_objs = 0
            Logger().debug(f'{self._name}: Sent {self._sent_objs}')
            return True

        return False

    async def send(self, item: Package) -> bool:
        Logger().info(f'''MockSink sent an object {item.payload.get_id()} '''
                      f'''with header destination {item.destination}''')
        self._sent_objs += 1
        return True
