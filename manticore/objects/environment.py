class Environment:
    def __init__(self):
        self._active: bool = False
        self._owned: bool = False

    @property
    def active(self) -> bool:
        return self._active

    @property
    def owned(self) -> bool:
        return self._owned
