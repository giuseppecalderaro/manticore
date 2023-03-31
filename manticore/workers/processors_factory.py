from typing import Dict, Type
from manticore.config.config import Config
from manticore.interfaces.factory import Factory
from manticore.utils.logger import Logger
from manticore.workers.generic_processor import GenericProcessor


class ProcessorsFactory(Factory):
    __processors: Dict[str, Type[GenericProcessor]] = {}

    @staticmethod
    def register(item: Type[GenericProcessor]) -> None:
        # The logger is not initialised yet, we can not use it here
        ProcessorsFactory.__processors[item.get_type()] = item

    @staticmethod
    def make(item_name: str, item_type: str, cfg: Config) -> GenericProcessor:
        if item_type in ProcessorsFactory.__processors:
            ret = ProcessorsFactory.__processors[item_type](item_name, cfg)
            Logger().info(f'ProcessorsFactory: built {item_type} with name {item_name}')
            return ret

        raise RuntimeError(f'ProcessorsFactory: CANNOT build {item_type} with name {item_name}')
