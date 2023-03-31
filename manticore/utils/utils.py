from typing import Any, Tuple
import base64
import mimetypes
import random
import string
import uuid
import numpy as np


def get_expanded_scientific_notation(flt: Any) -> str:
    values = str(flt).split('e')
    if len(values) == 1:
        return values[0]

    coef = float(values[0])
    exp = int(values[1])
    return_val = ''

    if int(exp) > 0:
        return_val += str(coef).replace('.', '')
        return_val += ''.join(['0' for _ in range(0, abs(exp - len(str(coef).split('.')[1])))])

    elif int(exp) < 0:
        return_val += '0.'
        return_val += ''.join(['0' for _ in range(0, abs(exp) - 1)])
        return_val += str(coef).replace('.', '')

    return return_val


def count_digits(number: Any, strip_trailing_zeros: bool = False) -> Tuple[int, int]:
    str_number = str(number).split('.')
    if strip_trailing_zeros:
        return len(str_number[0]), len(str_number[1].rstrip('0'))

    return len(str_number[0]), len(str_number[1])


### RANDOM STRING GENERATORS
def random_string_gen(size: int = 0, chars: str = string.printable) -> str:
    # We want a string with at least one character and at most 1000 character long
    if size == 0:
        size = np.random.randint(1, 1000)
    return ''.join(random.choice(chars) for _ in range(size))


def create_unique_identifier() -> Any:
    return uuid.uuid4().hex


### CONTENT ANALYZER
def init_content_type() -> None:
    # mimetypes.add_type('font/otf', '.otf')
    pass


def content_type(path_to_file: str) -> Any:
    return mimetypes.guess_type(path_to_file)[0]


### CONVERTERS AND TYPE CHECKERS
def is_integer(number: Any) -> bool:
    if isinstance(number, int):
        return True

    if isinstance(number, float):
        return number.is_integer()

    return False


def convert_to(number: Any, number_type: Any) -> Any:
    try:
        return number_type(number)
    except ValueError:
        return None


### ENCODERS/DECODERS
def convert_bytes_to_string(data: Any) -> str:
    if not isinstance(data, (bytes, bytearray)):
        return ''

    encoded = base64.b64encode(data)
    return encoded.decode('utf-8', 'strict')


def convert_string_to_bytes(data: str) -> bytes:
    if not isinstance(data, str):
        return b''

    return base64.b64decode(data.encode('utf-8'))
