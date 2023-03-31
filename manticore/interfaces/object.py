from typing import Any
from abc import ABC, abstractmethod


class Object(ABC):
    @abstractmethod
    def validate(self) -> bool:
        pass

    @abstractmethod
    def get_id(self) -> Any:
        pass

    @abstractmethod
    def get_timestamp(self) -> int:
        pass

    @classmethod
    @abstractmethod
    def get_type(cls) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_version() -> int:
        pass
