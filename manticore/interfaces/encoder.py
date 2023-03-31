from typing import Tuple
from abc import abstractmethod
from manticore.interfaces.component import Component
from manticore.objects.generic_object import Package


class Encoder(Component):
    @staticmethod
    @abstractmethod
    def is_compatible(mode: str) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def encode(package: Package) -> Tuple[bytes, int]:
        pass
