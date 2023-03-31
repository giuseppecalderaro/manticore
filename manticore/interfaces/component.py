from abc import ABC, abstractmethod


class Component(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_type() -> str:
        pass
