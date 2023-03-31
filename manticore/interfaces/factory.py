from typing import Any, Type
from abc import ABC, abstractmethod
from manticore.config.config import Config


class Factory(ABC):
    @staticmethod
    @abstractmethod
    def register(item: Type[Any]) -> None:
        pass

    @staticmethod
    @abstractmethod
    def make(item_name: str, item_type: str, cfg: Config) -> Any:
        pass
