from manticore.config.config import Config
from manticore.interfaces.encoder import Encoder


class GenericEncoder(Encoder):
    def __init__(self, name: str, cfg: Config):
        self._name = name
        self._cfg = cfg

    @property
    def name(self) -> str:
        return self._name
