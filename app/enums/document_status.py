from enum import Enum


class DocumentStatus(Enum):
    PENDING = 1
    PROCESSING = 2
    COMPLETED = 3
    FAILED = 4
