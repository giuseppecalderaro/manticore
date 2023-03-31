from enum import IntEnum


RAW_PAYLOAD = 'RawPayload'


class ResponseStatus(IntEnum):
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422  # This is used when the input is in the wrong format
    INTERNAL_ERROR = 500
    UNKNOWN_ERROR = 520
