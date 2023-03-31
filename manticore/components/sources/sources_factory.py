from typing import Dict, Type
from manticore.components.sources.generic_source import GenericSource
from manticore.config.config import Config
from manticore.interfaces.factory import Factory
from manticore.utils.logger import Logger


class SourcesFactory(Factory):
    __sources: Dict[str, Type[GenericSource]] = {}

    @staticmethod
    def register(item: Type[GenericSource]) -> None:
        # The logger is not initialised yet, we can not use it here
        SourcesFactory.__sources[item.get_type()] = item

    @staticmethod
    def make(item_name: str, item_type: str, cfg: Config) -> GenericSource:
        if item_type in SourcesFactory.__sources:
            ret = SourcesFactory.__sources[item_type](item_name, cfg)
            Logger().info(f'''SourcesFactory: built {item_type} with name {item_name}'''
                          f''' with decoder {ret.decoder_type()}''')
            return ret

        raise RuntimeError(f'SourcesFactory: CANNOT build {item_type} with name {item_name}')
