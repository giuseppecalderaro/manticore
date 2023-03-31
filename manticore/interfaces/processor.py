from abc import abstractmethod
from manticore.interfaces.component import Component
from manticore.objects.generic_object import Package


class Processor(Component):
    @staticmethod
    @abstractmethod
    def get_type() -> str:
        pass

    @property
    @abstractmethod
    def active(self) -> bool:
        pass

    @abstractmethod
    async def init(self) -> bool:
        pass

    @abstractmethod
    def run(self) -> bool:
        pass

    @abstractmethod
    async def process(self, item: Package) -> None:
        pass
