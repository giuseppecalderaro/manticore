from typing import Tuple
from manticore.components.encoders.generic_encoder import GenericEncoder
from manticore.objects.generic_object import Package


class CapnProtoEncoder(GenericEncoder):
    @staticmethod
    def get_type() -> str:
        return 'CapnProto'

    @staticmethod
    def is_compatible(mode: str) -> bool:
        return mode in ['binary']

    @staticmethod
    def encode(package: Package) -> Tuple[bytes, int]:
        pkg = package.to_capnproto()
        n_item = pkg.to_bytes()
        return n_item, len(n_item)
