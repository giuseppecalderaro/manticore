from manticore.config.config import Config
from manticore.interfaces.sink import Sink
from manticore.objects.generic_object import Package
from manticore.components.encoders.encoders_factory import EncodersFactory
from manticore.components.sinks.generic_sink_api import generic_sink_router


class GenericSink(Sink):
    def __init__(self, sink_name: str, cfg: Config):
        self._config = cfg
        self._name = sink_name
        self._flush_threshold = cfg.get(sink_name, 'flush_threshold')
        self._allowed_sources = cfg.get(sink_name, 'allowed_sources')

        encoder_type = cfg.get(sink_name, 'encoder')
        self._encoder = EncodersFactory.make(encoder_type, encoder_type, cfg)
        if not self._encoder:
            raise RuntimeError(f'Cannot initialise encoder {encoder_type} in sink {sink_name}')

        # Initialise interface
        from manticore.workers.generic_api import processor_api
        processor_api.include_router(generic_sink_router, prefix=f'/{self._name}', tags=[self.name])

    @property
    def name(self) -> str:
        return self._name

    def encoder_type(self) -> str:
        return self._encoder.get_type()

    async def complete(self) -> bool:
        return False

    def should_send(self, item: Package) -> bool:
        if not self._allowed_sources:
            # we allow everything if the field is missing
            return True

        if item.source in self._allowed_sources:
            return True

        return False
