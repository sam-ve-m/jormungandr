# Third party
from strenum import StrEnum


class ImageExtension(StrEnum):
    banner = "banner"
    logo = "logo"
    thumbnail = "thumbnail"

    def __repr__(self):
        return self.value
