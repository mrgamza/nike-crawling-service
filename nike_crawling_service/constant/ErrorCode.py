from enum import Enum, auto


class ErrorCode(Enum):
    SUCCESS = '0000'
    RESPONSE_ERROR = '1000'
    KNOWN_ERROR = '9000'