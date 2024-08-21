# Standards
from enum import IntEnum


class QueueTypes(IntEnum):
    PROSPECT_USER = 0

    def __repr__(self):
        return self.value
