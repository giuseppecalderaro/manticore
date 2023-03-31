from manticore.config.config import Config
from manticore.interfaces.model import Model


class GenericModel(Model):
    @classmethod
    def get_type(cls) -> str:
        return cls.__name__

    def __init__(self, model_name: str, cfg: Config):
        self._name = model_name
        self._config = cfg

        # Initialise interface
        from manticore.analytics.generic_model_api import generic_model_router
        from manticore.workers.generic_api import processor_api
        processor_api.include_router(generic_model_router, prefix=f'/{self.name}', tags=[self.name])

    @property
    def name(self) -> str:
        return self._name
