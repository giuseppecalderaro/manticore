from typing import Tuple
from manticore.components.encoders.generic_encoder import GenericEncoder
from manticore.objects.generic_object import Package


class ProtobufEncoder(GenericEncoder):
    @staticmethod
    def get_type() -> str:
        return 'Protobuf'

    @staticmethod
    def is_compatible(mode: str) -> bool:
        return mode in ['binary']

    @staticmethod
    def encode(package: Package) -> Tuple[bytes, int]:
        pkg = package.to_protobuf()
        n_item = pkg.SerializeToString()
        return n_item, len(n_item)
