from typing import Dict, Type
from manticore.components.sinks.generic_sink import GenericSink
from manticore.config.config import Config
from manticore.interfaces.factory import Factory
from manticore.utils.logger import Logger


class SinksFactory(Factory):
    __sinks: Dict[str, Type[GenericSink]] = {}

    @staticmethod
    def register(item: Type[GenericSink]) -> None:
        # The logger is not initialised yet, we can not use it here
        SinksFactory.__sinks[item.get_type()] = item

    @staticmethod
    def make(item_name: str, item_type: str, cfg: Config) -> GenericSink:
        if item_type in SinksFactory.__sinks:
            ret = SinksFactory.__sinks[item_type](item_name, cfg)
            Logger().info(f'''SinksFactory: built {item_type}'''
                          f''' with name {item_name} with encoder {ret.encoder_type()}''')
            return ret

        raise RuntimeError(f'SinksFactory: CANNOT build {item_type} with name {item_name}')
