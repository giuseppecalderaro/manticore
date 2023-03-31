from typing import Dict, Type
from manticore.components.encoders.generic_encoder import GenericEncoder
from manticore.config.config import Config
from manticore.interfaces.factory import Factory
from manticore.utils.logger import Logger


class EncodersFactory(Factory):
    __encoders: Dict[str, Type[GenericEncoder]] = {}

    @staticmethod
    def register(item: Type[GenericEncoder]) -> None:
        # The logger is not initialised yet, we can not use it here
        EncodersFactory.__encoders[item.get_type()] = item

    @staticmethod
    def make(item_name: str, item_type: str, cfg: Config) -> GenericEncoder:
        if item_type in EncodersFactory.__encoders:
            ret = EncodersFactory.__encoders[item_type](item_name, cfg)
            Logger().info(f'EncodersFactory: built {item_type} with name {item_name}')
            return ret

        raise RuntimeError(f'EncodersFactory: CANNOT build {item_type} with name {item_name}')
