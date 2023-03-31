import asyncio
import itertools
from manticore.analytics.models_factory import ModelsFactory
from manticore.config.config import Config
from manticore.objects.environment import Environment
from manticore.objects.generic_object import Package
from manticore.utils.lag_detector import LagDetector
from manticore.utils.logger import Logger
from manticore.workers.generic_processor import GenericProcessor


class ProcessingEngine(GenericProcessor):
    @staticmethod
    def get_type() -> str:
        return 'ProcessingEngine'

    def __init__(self, processor_name: str, cfg: Config):
        super().__init__(processor_name, cfg)
        self.models = {}
        self._processing = True
        self._env = Environment()

        models_names = cfg.get(processor_name, 'models')
        for model_name in models_names:
            model_type = cfg.get(model_name, 'type')
            self.models[model_name] = ModelsFactory.make(model_name, model_type, cfg)

        # Initialise interface
        from manticore.workers.processing_engine.processing_engine_api import processing_engine_router
        from manticore.workers.generic_api import processor_api
        processor_api.include_router(processing_engine_router, prefix=f'/{self.name}', tags=[self.name])

    async def init(self) -> bool:
        active = await super().init()

        for _, model in self.models.items():
            Logger().info(f'Initialising {model.name}')
            if await model.init():
                Logger().info('Done')
            else:
                Logger().info('Failed')

        return active

    async def process(self, item: Package) -> None:
        if self.models:
            # Execute all strategies
            coros_exe = [model.execute(item, self._env) for model in self.models.values()]
            models_output = await asyncio.gather(*coros_exe, return_exceptions=False)

            # TODO-GSC: check for exceptions in the results
            coros = [self._out_q.put(obj) for obj in \
                list(itertools.chain.from_iterable(models_output))]
            await asyncio.gather(*coros)

        Logger().debug(f'Lag: {LagDetector().object_lag(item.payload)}')
