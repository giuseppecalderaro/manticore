from typing import List
from abc import abstractmethod
from manticore.interfaces.component import Component
from manticore.objects.environment import Environment
from manticore.objects.generic_object import Package


class Model(Component):
    @abstractmethod
    async def init(self) -> bool:
        pass

    @abstractmethod
    async def execute(self, item: Package, environment: Environment) -> List[Package]:
        pass
