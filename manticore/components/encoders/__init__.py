### Factory
from manticore.components.encoders.encoders_factory import EncodersFactory
from manticore.components.encoders.capnproto_encoder.capnproto_encoder import CapnProtoEncoder
from manticore.components.encoders.json_encoder.json_encoder import JsonEncoder
from manticore.components.encoders.protobuf_encoder.protobuf_encoder import ProtobufEncoder

### CapnProto encoder
EncodersFactory.register(CapnProtoEncoder)

### JSON encoder
EncodersFactory.register(JsonEncoder)

### Protobuf encoder
EncodersFactory.register(ProtobufEncoder)
