from pydantic import BaseModel

from func.src.domain.enums.region.enum import Region


class WatchListProduct(BaseModel):
    product_id: int
    region: Region
