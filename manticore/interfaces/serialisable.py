from typing import Any, Dict
from abc import ABC, abstractmethod


class CapnProtoSerialisable(ABC):
    @classmethod
    @abstractmethod
    def from_capnproto(cls, n_item: Any) -> Any:
        pass

    @abstractmethod
    def to_capnproto(self) -> Any:
        pass


class JsonSerialisable(ABC):
    @classmethod
    @abstractmethod
    def from_json(cls, n_item: Dict[str, Any]) -> Any:
        pass

    @abstractmethod
    def to_json(self, add_metadata: bool) -> Dict[str, Any]:
        pass


class ProtobufSerialisable(ABC):
    @classmethod
    @abstractmethod
    def from_protobuf(cls, n_item: Any) -> Any:
        pass

    @abstractmethod
    def to_protobuf(self) -> Any:
        pass
