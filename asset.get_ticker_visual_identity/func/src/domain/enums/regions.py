# Third party
from strenum import StrEnum


class RegionOptions(StrEnum):
    BR = "BR"
    US = "US"

    def __repr__(self):
        return self.value
