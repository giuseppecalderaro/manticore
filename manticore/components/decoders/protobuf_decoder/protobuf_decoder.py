from manticore.components.decoders.generic_decoder import GenericDecoder
from manticore.objects.generic_object import Package
import manticore.generated.common_pb2 as pb


class ProtobufDecoder(GenericDecoder):
    @staticmethod
    def get_type() -> str:
        return 'Protobuf'

    @staticmethod
    def is_compatible(mode: str) -> bool:
        return mode in ['binary']

    @staticmethod
    def decode(package: bytes) -> Package:
        pkg_pb = pb.package()
        pkg_pb.ParseFromString(package)

        pkg = Package.from_protobuf(pkg_pb)
        return pkg
