from __future__ import annotations
from typing import Any, cast, Dict, Mapping
import os
import capnp
from manticore.objects.generic_object import GenericObject
from manticore.utils.logger import Logger
import manticore.generated.messages_pb2 as pb


MESSAGES_CAPNP = capnp.load(os.path.dirname(__file__) + '/../../interfaces/capnp/messages.capnp')


class MockV1(GenericObject):
    @staticmethod
    def get_version() -> int:
        return 1

    @classmethod
    def build(cls, obj_id: Any, timestamp: int, data: str) -> MockV1:
        obj = cls(obj_id, timestamp)
        obj.data = data

        if not obj.validate():
            raise RuntimeError('MockV1: validation failed')

        return obj

    @classmethod
    def from_capnproto(cls, n_item: Any) -> MockV1:
        n_item = n_item.as_struct(MESSAGES_CAPNP.MockV1)
        obj = cast(MockV1, super().from_capnproto(n_item.obj))
        obj.data = n_item.data

        if not obj.validate():
            raise RuntimeError('MockV1: validation failed')

        return obj

    @classmethod
    def from_json(cls, n_item: Mapping[str, Any]) -> MockV1:
        obj = cast(MockV1, super().from_json(n_item))
        obj.data = n_item['data']

        if not obj.validate():
            raise RuntimeError('MockV1: validation failed')

        return obj

    @classmethod
    def from_protobuf(cls, n_item: bytes) -> MockV1:
        mock_pb = pb.mock_v1()
        mock_pb.ParseFromString(n_item)
        obj = cast(MockV1, super().from_protobuf(mock_pb.obj))
        obj.data = mock_pb.data

        if not obj.validate():
            raise RuntimeError('MockV1: validation failed')

        return obj

    def __init__(self, obj_id: Any, timestamp: int):
        super().__init__(obj_id, timestamp)
        self.data = cast(str, None)

    def validate(self) -> bool:
        if not super().validate():
            return False

        if not isinstance(self.data, str):
            Logger().error(f'MockV1::data is a {type(self.data)} instead of a {str}')
            return False

        return True

    def to_capnproto(self) -> Any:
        msg = MESSAGES_CAPNP.MockV1.new_message()
        msg.obj = super().to_capnproto()
        msg.data = self.data
        return msg

    def to_json(self, add_metadata: bool = None) -> Dict[str, Any]:
        msg = super().to_json(add_metadata)
        msg['data'] = self.data
        return msg

    def to_protobuf(self) -> Any:
        msg = pb.mock_v1()

        ### The line below fails on aarch64
        # msg.obj.CopyFrom(super().to_protobuf())
        ### The line below works both on x86_64 and aarch64 but it is slower
        msg.obj.ParseFromString(super().to_protobuf().SerializeToString())

        msg.data = self.data
        return msg


class MockV2(GenericObject):
    @staticmethod
    def get_version() -> int:
        return 1

    @classmethod
    def build(cls, obj_id: Any, timestamp: int, data: str, data2: str) -> MockV2:
        obj = cls(obj_id, timestamp)
        obj.data = data
        obj.data2 = data2

        if not obj.validate():
            raise RuntimeError('MockV2: validation failed')

        return obj

    @classmethod
    def from_capnproto(cls, n_item: Any) -> MockV2:
        n_item = n_item.as_struct(MESSAGES_CAPNP.MockV2)
        obj = cast(MockV2, super().from_capnproto(n_item.obj))
        obj.data = n_item.data
        obj.data2 = n_item.data2

        if not obj.validate():
            raise RuntimeError('MockV2: validation failed')

        return obj

    @classmethod
    def from_json(cls, n_item: Mapping[str, Any]) -> MockV2:
        obj = cast(MockV2, super().from_json(n_item))
        obj.data = n_item['data']
        obj.data2 = n_item['data2']

        if not obj.validate():
            raise RuntimeError('MockV2: validation failed')

        return obj

    @classmethod
    def from_protobuf(cls, n_item: bytes) -> MockV2:
        mock_pb = pb.mock_v2()
        mock_pb.ParseFromString(n_item)
        obj = cast(MockV2, super().from_protobuf(mock_pb.obj))
        obj.data = mock_pb.data
        obj.data2 = mock_pb.data2

        if not obj.validate():
            raise RuntimeError('MockV2: validation failed')

        return obj

    def __init__(self, obj_id: Any, timestamp: int):
        super().__init__(obj_id, timestamp)
        self.data = cast(str, None)
        self.data2 = cast(str, None)

    def validate(self) -> bool:
        if not super().validate():
            return False

        if not isinstance(self.data, str):
            Logger().error(f'MockV2::data is a {type(self.data)} instead of a {str}')
            return False

        if not isinstance(self.data2, str):
            Logger().error(f'MockV2::data2 is a {type(self.data2)} instead of a {str}')
            return False

        return True

    def to_capnproto(self) -> Any:
        msg = MESSAGES_CAPNP.MockV2.new_message()
        msg.obj = super().to_capnproto()
        msg.data = self.data
        msg.data2 = self.data2
        return msg

    def to_json(self, add_metadata: bool = None) -> Dict[str, Any]:
        msg = super().to_json(add_metadata)
        msg['data'] = self.data
        msg['data2'] = self.data2
        return msg

    def to_protobuf(self) -> Any:
        msg = pb.mock_v2()

        ### The line below fails on aarch64
        # msg.obj.CopyFrom(super().to_protobuf())
        ### The line below works both on x86_64 and aarch64 but it is slower
        msg.obj.ParseFromString(super().to_protobuf().SerializeToString())

        msg.data = self.data
        msg.data2 = self.data2
        return msg
