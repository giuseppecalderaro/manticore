from manticore.config.config import Config
from manticore.interfaces.decoder import Decoder


class GenericDecoder(Decoder):
    def __init__(self, name: str, cfg: Config):
        self._name = name
        self._cfg = cfg

    @property
    def name(self) -> str:
        return self._name
