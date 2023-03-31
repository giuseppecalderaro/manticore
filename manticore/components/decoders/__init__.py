### Factory
from manticore.components.decoders.decoders_factory import DecodersFactory
from manticore.components.decoders.capnproto_decoder.capnproto_decoder import CapnProtoDecoder
from manticore.components.decoders.json_decoder.json_decoder import JsonDecoder
from manticore.components.decoders.protobuf_decoder.protobuf_decoder import ProtobufDecoder

### CapnProto decoder
DecodersFactory.register(CapnProtoDecoder)

### JSON decoder
DecodersFactory.register(JsonDecoder)

### Protobuf decoder
DecodersFactory.register(ProtobufDecoder)
