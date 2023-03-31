from __future__ import annotations
from typing import Any, cast, Dict, Mapping, Optional
import os
import capnp
from pydantic import BaseModel
from manticore.interfaces.enums import RAW_PAYLOAD, ResponseStatus
from manticore.interfaces.object import Object
from manticore.interfaces.serialisable import CapnProtoSerialisable, \
                                              JsonSerialisable, \
                                              ProtobufSerialisable
from manticore.utils.logger import Logger
import manticore.utils.time_utils as tu
import manticore.generated.common_pb2 as pb


COMMON_CAPNP = capnp.load(os.path.dirname(__file__) + '/../interfaces/capnp/common.capnp')


class Package(CapnProtoSerialisable, JsonSerialisable, ProtobufSerialisable):
    @classmethod
    def from_capnproto(cls, n_item: Any) -> Package:
        obj_type = n_item.objType
        obj_version = n_item.objVersion
        source = n_item.source
        destination = n_item.destination
        payload = n_item.payload

        if obj_type != RAW_PAYLOAD:
            from manticore.objects.objects_factory import ObjectsFactory
            obj_cls = cast(CapnProtoSerialisable, ObjectsFactory.make(obj_type, obj_version))
            payload = obj_cls.from_capnproto(payload)

        return cls(obj_type, obj_version, source, destination, payload)

    @classmethod
    def from_json(cls, n_item: Mapping[str, Any]) -> Package:
        obj_type = n_item['type']
        obj_version = n_item['version']
        payload = n_item['payload']

        if obj_type != RAW_PAYLOAD:
            from manticore.objects.objects_factory import ObjectsFactory
            obj_cls = cast(JsonSerialisable, ObjectsFactory.make(obj_type, obj_version))
            payload = obj_cls.from_json(payload)

        return cls(obj_type,
                   obj_version,
                   n_item['source'],
                   n_item['destination'],
                   payload)

    @classmethod
    def from_protobuf(cls, n_item: Any) -> Package:
        obj_type = n_item.obj_type
        obj_version = n_item.obj_version
        source = n_item.source
        destination = n_item.destination
        payload = n_item.payload.value

        if obj_type != RAW_PAYLOAD:
            from manticore.objects.objects_factory import ObjectsFactory
            obj_cls = cast(ProtobufSerialisable, ObjectsFactory.make(obj_type, obj_version))
            payload = obj_cls.from_protobuf(payload)

        return cls(obj_type, obj_version, source, destination, payload)

    def __init__(self,
                 obj_type: str,
                 obj_version: int,
                 source: str,
                 destination: str,
                 payload: Any):
        self._obj_type = obj_type
        self._obj_version = obj_version
        self._source = source
        self._destination = destination
        self._payload = payload

    @property
    def obj_type(self) -> str:
        return self._obj_type

    @property
    def obj_version(self) -> int:
        return self._obj_version

    @property
    def source(self) -> str:
        return self._source

    @property
    def destination(self) -> str:
        return self._destination

    @property
    def payload(self) -> Any:
        return self._payload

    def to_capnproto(self) -> Any:
        pkg = COMMON_CAPNP.Package.new_message()
        pkg.objType = self._obj_type
        pkg.objVersion = self._obj_version
        pkg.source = self._source
        pkg.destination = self._destination

        msg = self._payload
        if self._obj_type != RAW_PAYLOAD:
            msg = self._payload.to_capnproto()
        pkg.payload = msg

        return pkg

    def to_json(self, add_metadata=True) -> Dict[str, Any]:
        pkg: Dict[str, Any] = {}
        pkg['type'] = self._obj_type
        pkg['version'] = self._obj_version
        pkg['destination'] = self._destination
        pkg['source'] = self._source

        payload: Any = self._payload
        if self._obj_type != RAW_PAYLOAD:
            payload = payload.to_json(add_metadata)
        pkg['payload'] = payload

        return pkg

    def to_protobuf(self) -> Any:
        pkg = pb.package()
        pkg.obj_type = self._obj_type
        pkg.obj_version = self._obj_version
        pkg.source = self._source
        pkg.destination = self._destination

        msg = self._payload
        if self._obj_type != RAW_PAYLOAD:
            msg = self._payload.to_protobuf()
        pkg.payload.Pack(msg)

        return pkg


class GenericObject(Object, CapnProtoSerialisable, JsonSerialisable, ProtobufSerialisable):
    class GenericObjectModel(BaseModel):
        id: Optional[Any]
        timestamp: Optional[int]

    @classmethod
    def get_type(cls) -> str:
        return cls.__name__

    @classmethod
    def from_capnproto(cls, n_item: Any) -> GenericObject:
        return cls(n_item.id, n_item.timestamp)

    @classmethod
    def from_json(cls, n_item: Mapping[str, Any]) -> GenericObject:
        return cls(n_item.get('id', None), n_item.get('timestamp', 0))

    @classmethod
    def from_protobuf(cls, n_item: Any) -> GenericObject:
        return cls(n_item.id, n_item.timestamp)

    @classmethod
    def from_db(cls, n_item) -> GenericObject:
        timestamp = n_item.modified_at if n_item.modified_at else n_item.created_at
        return cls(n_item.id,
                   tu.datetime_to_timestamp_us(str(timestamp)))

    def __init__(self, obj_id: Any, timestamp: int):
        self._id = obj_id
        self._timestamp = timestamp

    def validate(self) -> bool:
        ### We do not check the id as that might be
        ### either a string or an integer

        if not isinstance(self._timestamp, int):
            Logger().error(f'GenericObject::filters is a {type(self._timestamp)} instead of a {int}')
            return False

        return True

    def get_id(self) -> Any:
        return self._id

    def get_timestamp(self) -> int:
        return self._timestamp

    def to_capnproto(self) -> Any:
        obj = COMMON_CAPNP.Object.new_message()
        obj.id = self._id
        obj.timestamp = self._timestamp
        return obj

    def to_json(self, add_metadata: bool = True) -> Dict[str, Any]:
        obj: Dict[str, Any] = {}

        if add_metadata:
            if self._id:
                obj['id'] = self._id

            if self._timestamp:
                obj['timestamp'] = self._timestamp

        return obj

    def to_protobuf(self) -> Any:
        obj = pb.object()
        obj.id = self._id
        obj.timestamp = self._timestamp
        return obj


class GenericRequest(GenericObject):
    @classmethod
    def _build(cls, obj_id: Any, timestamp: int, filters: Mapping[str, Any]) -> GenericRequest:
        obj = cls(obj_id, timestamp)
        obj.filters = filters
        return obj

    @classmethod
    def from_capnproto(cls, n_item: bytes) -> GenericRequest:
        request_cnp = COMMON_CAPNP.Request.from_bytes(n_item)
        obj = cast(GenericRequest, super().from_capnproto(request_cnp.obj))
        obj.filters = {}  # TODO-GSC: complete populating filters
        return obj

    @classmethod
    def from_json(cls, n_item: Mapping[str, Any]) -> GenericRequest:
        obj = cast(GenericRequest, super().from_json(n_item))
        obj.filters = cast(Dict[str, Any], n_item['filters'])
        return obj

    @classmethod
    def from_protobuf(cls, n_item: bytes) -> GenericRequest:
        request_pb = pb.request()
        request_pb.ParseFromString(n_item)
        obj = cast(GenericRequest, super().from_protobuf(request_pb.obj))
        obj.filters = {}  # TODO-GSC: complete populating filters
        return obj

    def __init__(self, obj_id: Any, timestamp: int):
        super().__init__(obj_id, timestamp)
        self.filters = cast(Mapping[str, Any], None)

    def validate(self) -> bool:
        if not super().validate():
            return False

        if not isinstance(self.filters, dict):
            Logger().error(f'GenericRequest::filters is a {type(self.filters)} instead of a {dict}')
            return False

        return True

    def to_capnproto(self) -> Any:
        msg = COMMON_CAPNP.Request.new_message()
        msg.obj = super().to_capnproto()
        msg.filters = {}  # TODO-GSC: complete populating filters
        return msg

    def to_json(self, add_metadata=True) -> Dict[str, Any]:
        obj = super().to_json(add_metadata)
        obj['filters'] = self.filters
        return obj

    def to_protobuf(self) -> Any:
        msg = pb.request()
        msg.obj.CopyFrom(super().to_protobuf())
        msg.filters = {}  # TODO-GSC: complete populating filters
        return msg


class GenericResponse(GenericObject):
    @classmethod
    def _build(cls,
               obj_id: Any,
               timestamp: int,
               status: ResponseStatus,
               detail: str) -> GenericResponse:
        obj = cls(obj_id, timestamp)
        obj.status = status
        obj.detail = detail
        return obj

    @classmethod
    def from_capnproto(cls, n_item: bytes) -> GenericResponse:
        response_cnp = COMMON_CAPNP.Response.from_bytes(n_item)
        obj = cast(GenericResponse, super().from_capnproto(response_cnp.obj))
        obj.status = response_cnp.status
        obj.detail = response_cnp.detail
        return obj

    @classmethod
    def from_json(cls, n_item: Mapping[str, Any]) -> GenericResponse:
        obj = cast(GenericResponse, super().from_json(n_item))
        obj.status = n_item['status']
        obj.detail = n_item['detail']
        return obj

    @classmethod
    def from_protobuf(cls, n_item: bytes) -> GenericResponse:
        response_pb = pb.response()
        response_pb.ParseFromString(n_item)
        obj = cast(GenericResponse, super().from_protobuf(response_pb.obj))
        obj.status = response_pb.status
        obj.detail = response_pb.detail
        return obj

    def __init__(self, obj_id: Any, timestamp: int):
        super().__init__(obj_id, timestamp)
        self.status = cast(ResponseStatus, None)
        self.detail = cast(str, None)

    def validate(self) -> bool:
        if not super().validate():
            return False

        if not isinstance(self.status, int):
            Logger().error(f'GenericResponse::status is a {type(self.status)} instead of a {int}')
            return False

        if not isinstance(self.detail, str):
            Logger().error(f'GenericResponse::detail is a {type(self.detail)} instead of a {str}')
            return False

        return True

    def to_capnproto(self) -> Any:
        msg = COMMON_CAPNP.Response.new_message()
        msg.obj = super().to_capnproto()
        msg.status = int(self.status)
        msg.detail = self.detail
        return msg

    def to_json(self, add_metadata=True) -> Dict[str, Any]:
        obj = super().to_json(add_metadata)
        obj['status'] = int(self.status)
        obj['detail'] = self.detail
        return obj

    def to_protobuf(self) -> Any:
        msg = pb.response()
        msg.obj.CopyFrom(super().to_protobuf())
        msg.status = int(self.status)
        msg.detail = self.detail
        return msg
