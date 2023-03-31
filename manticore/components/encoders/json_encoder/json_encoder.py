from typing import Tuple
import orjson as json
from manticore.components.encoders.generic_encoder import GenericEncoder
from manticore.objects.generic_object import Package


class JsonEncoder(GenericEncoder):
    @staticmethod
    def get_type() -> str:
        return 'Json'

    @staticmethod
    def is_compatible(mode: str) -> bool:
        return mode in ['binary', 'text']

    @staticmethod
    def encode(package: Package) -> Tuple[bytes, int]:
        pkg_dict = package.to_json()
        n_item = json.dumps(pkg_dict)
        return n_item, len(n_item)
