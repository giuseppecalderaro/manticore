from abc import abstractmethod
from manticore.interfaces.component import Component
from manticore.objects.generic_object import Package


class Sink(Component):
    @abstractmethod
    async def init(self) -> bool:
        pass

    @abstractmethod
    async def send(self, item: Package) -> bool:
        pass

    @abstractmethod
    async def complete(self) -> bool:
        pass

    @abstractmethod
    def should_send(self, item: Package) -> bool:
        pass
