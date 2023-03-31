from typing import Dict, Type
from manticore.analytics.generic_model import GenericModel
from manticore.config.config import Config
from manticore.interfaces.factory import Factory
from manticore.utils.logger import Logger


class ModelsFactory(Factory):
    __models: Dict[str, Type[GenericModel]] = {}

    @staticmethod
    def register(item: Type[GenericModel]) -> None:
        # The logger is not initialised yet, we can not use it here
        ModelsFactory.__models[item.get_type()] = item

    @staticmethod
    def make(item_name: str, item_type: str, cfg: Config) -> GenericModel:
        if item_type in ModelsFactory.__models:
            ret = ModelsFactory.__models[item_type](item_name, cfg)
            Logger().info(f'ModelsFactory: built {item_type} with name {item_name}')
            return ret

        raise RuntimeError(f'ModelsFactory: CANNOT build {item_type} with name {item_name}')
