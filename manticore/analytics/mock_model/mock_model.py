from typing import List
from manticore.analytics.generic_model import GenericModel
from manticore.config.config import Config
from manticore.objects.environment import Environment
from manticore.objects.generic_object import Package
from manticore.utils.logger import Logger


class MockModel(GenericModel):
    def __init__(self, model_name: str, cfg: Config):
        super().__init__(model_name, cfg)
        self.processed_items = 0

        # Initialise interface
        from manticore.analytics.mock_model.mock_model_api import mock_model_router
        from manticore.workers.generic_api import processor_api
        processor_api.include_router(mock_model_router, prefix=f'/{self.name}', tags=[self.name])

    async def init(self) -> bool:
        Logger().info('Initialised MockModel')
        return True

    async def execute(self, item: Package, environment: Environment) -> List[Package]:
        ret = []

        Logger().info(f'MockModel processed item {type(item.payload)}')
        ret.append(item)
        self.processed_items += 1

        return ret
