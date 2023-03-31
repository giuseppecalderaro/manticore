from manticore.interfaces.object import Object
from manticore.utils.logger import Logger
import manticore.utils.time_utils as tutil


class LagDetector:
    class InternalLagDetector:
        def __init__(self):
            pass

        def unused1(self) -> None:
            pass

        def unused2(self) -> None:
            pass

    instance = None

    @staticmethod
    def timestamp_lag(tstamp: int, printer: bool = True) -> int:
        now = tutil.now_us()
        lag = now - tstamp
        if printer:
            Logger().debug(f'LagDetector: {tutil.timestamp_us_to_datetime(now)} - '
                           f'{tutil.timestamp_us_to_datetime(tstamp)} = {lag}')
        return lag

    def __init__(self):
        if not LagDetector.instance:
            LagDetector.instance = LagDetector.InternalLagDetector()

    def datetime_lag(self, dtime: str, printer: bool = True) -> int:
        tstamp = tutil.datetime_to_timestamp_us(dtime)
        return self.timestamp_lag(tstamp, printer)

    def object_lag(self, obj: Object, printer: bool = True) -> int:
        return self.timestamp_lag(obj.get_timestamp(), printer)
