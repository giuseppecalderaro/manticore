from manticore.config.config import Config
from manticore.objects.generic_object import Package
from manticore.workers.generic_processor import GenericProcessor


class Runner(GenericProcessor):
    @staticmethod
    def get_type() -> str:
        return 'Runner'

    def __init__(self, processor_name: str, cfg: Config):
        super().__init__(processor_name, cfg)
        self._processing = False

        # Initialise interface
        from manticore.workers.runner.runner_api import runner_router
        from manticore.workers.generic_api import processor_api
        processor_api.include_router(runner_router, prefix=f'/{self.name}', tags=[self.name])

    async def process(self, item: Package) -> None:
        await self._out_q.put(item)
