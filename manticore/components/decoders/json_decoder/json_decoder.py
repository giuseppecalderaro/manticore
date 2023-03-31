import orjson as json
from manticore.components.decoders.generic_decoder import GenericDecoder
from manticore.objects.generic_object import Package


class JsonDecoder(GenericDecoder):
    @staticmethod
    def get_type() -> str:
        return 'Json'

    @staticmethod
    def is_compatible(mode: str) -> bool:
        return mode in ['binary', 'text']

    @staticmethod
    def decode(package: bytes) -> Package:
        pkg_dict = json.loads(package)
        pkg = Package.from_json(pkg_dict)
        return pkg
