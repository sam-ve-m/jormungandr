# Jormungandr
from ...domain.enums.regions import RegionOptions
from ...domain.enums.images import ImageExtension

# Third party
from pydantic import BaseModel, Extra


class Ticker(BaseModel, extra=Extra.forbid):
    symbol: str
    region: RegionOptions
    type: ImageExtension
