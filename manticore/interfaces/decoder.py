from abc import abstractmethod
from manticore.interfaces.component import Component
from manticore.objects.generic_object import Package


class Decoder(Component):
    @staticmethod
    @abstractmethod
    def is_compatible(mode: str) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def decode(package: bytes) -> Package:
        pass
