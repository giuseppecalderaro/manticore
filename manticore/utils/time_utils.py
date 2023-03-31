from typing import Optional, Union
import datetime
import time
import ciso8601


def append_datetime(string: str) -> str:
    timestr = time.strftime('%Y%m%d-%H%M%S')
    return string + '_' + timestr


def append_date(string: str) -> str:
    timestr = time.strftime('%Y%m%d')
    return string + '_' + timestr


def datetime_to_timestamp_us(input_datetime: Optional[str]) -> int:
    if not input_datetime:
        return 0

    parsed_datetime = ciso8601.parse_datetime(input_datetime)
    tstamp = parsed_datetime.timestamp()
    return int(tstamp * 1000000)


def timestamp_to_datetime(tstamp: Optional[Union[int, float]]) -> Optional[datetime.datetime]:
    if not tstamp:
        return None

    return datetime.datetime.fromtimestamp(tstamp)


def timestamp_ms_to_datetime(tstamp: Union[int, float]) -> Optional[datetime.datetime]:
    return timestamp_to_datetime(tstamp / 1000.0)


def timestamp_us_to_datetime(tstamp: Union[int, float]) -> Optional[datetime.datetime]:
    return timestamp_to_datetime(tstamp / 1000000.0)


def now() -> int:
    dtime = datetime.datetime.now()
    tstamp = dtime.timestamp()
    return int(tstamp)


def now_ms() -> int:
    return now() * 1000


def now_us() -> int:
    return now() * 1000000


def delta_us(datetime_1: datetime.datetime, datetime_2: datetime.datetime) -> int:
    delta = datetime_1 - datetime_2
    return int(delta.total_seconds() * 1000000)
