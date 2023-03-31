from typing import Dict, Type
from manticore.components.decoders.generic_decoder import GenericDecoder
from manticore.config.config import Config
from manticore.interfaces.factory import Factory
from manticore.utils.logger import Logger


class DecodersFactory(Factory):
    __decoders: Dict[str, Type[GenericDecoder]] = {}

    @staticmethod
    def register(item: Type[GenericDecoder]) -> None:
        # The logger is not initialised yet, we can not use it here
        DecodersFactory.__decoders[item.get_type()] = item

    @staticmethod
    def make(item_name: str, item_type: str, cfg: Config) -> GenericDecoder:
        if item_type in DecodersFactory.__decoders:
            ret = DecodersFactory.__decoders[item_type](item_name, cfg)
            Logger().info(f'DecodersFactory: built {item_type} with name {item_name}')
            return ret

        raise RuntimeError(f'DecodersFactory: CANNOT build {item_type} with name {item_name}')
