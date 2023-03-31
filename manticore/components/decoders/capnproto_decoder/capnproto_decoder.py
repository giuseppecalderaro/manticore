import os
import capnp
from manticore.components.decoders.generic_decoder import GenericDecoder
from manticore.objects.generic_object import Package


COMMON_CAPNP = capnp.load(os.path.dirname(__file__) + '/../../../interfaces/capnp/common.capnp')


class CapnProtoDecoder(GenericDecoder):
    @staticmethod
    def get_type() -> str:
        return 'CapnProto'

    @staticmethod
    def is_compatible(mode: str) -> bool:
        return mode in ['binary']

    @staticmethod
    def decode(package: bytes) -> Package:
        pkg_cnp = COMMON_CAPNP.Package.from_bytes(package)
        pkg = Package.from_capnproto(pkg_cnp)
        return pkg
