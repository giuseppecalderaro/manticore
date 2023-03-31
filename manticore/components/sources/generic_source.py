from manticore.config.config import Config
from manticore.interfaces.source import Source
from manticore.components.decoders.decoders_factory import DecodersFactory
from manticore.components.sources.generic_source_api import generic_source_router


class GenericSource(Source):
    def __init__(self, source_name: str, cfg: Config):
        self._config = cfg
        self._valid = False
        self._name = source_name

        self._is_generator = False
        self._allowed_types = cfg.get(source_name, 'allowed_types')
        if self._allowed_types:
            self._allowed_types = set(self._allowed_types)

        decoder_type = cfg.get(source_name, 'decoder')
        self._decoder = DecodersFactory.make(decoder_type, decoder_type, cfg)
        if not self._decoder:
            raise RuntimeError(f'Cannot initialise decoder {decoder_type} in source {source_name}')

        # Initialise interface
        from manticore.workers.generic_api import processor_api
        processor_api.include_router(generic_source_router, prefix=f'/{self._name}', tags=[self.name])

    @property
    def name(self) -> str:
        return self._name

    @property
    def valid(self) -> bool:
        return self._valid

    @property
    def is_generator(self) -> bool:
        return self._is_generator

    def decoder_type(self) -> str:
        return self._decoder.get_type()
