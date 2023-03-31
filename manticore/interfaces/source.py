from abc import abstractmethod
from manticore.interfaces.component import Component


class Source(Component):
    @property
    @abstractmethod
    def valid(self) -> bool:
        pass

    @property
    @abstractmethod
    def is_generator(self) -> bool:
        pass

    @abstractmethod
    def decoder_type(self) -> str:
        pass

    @abstractmethod
    async def init(self) -> bool:
        pass

    ### There's no return type as recv()
    ### can either return an object or
    ### an async iterable
    @abstractmethod
    async def recv(self):
        pass
