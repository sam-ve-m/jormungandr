from func.src.domain.enums.region.enum import Region

from pydantic import BaseModel, constr, validator


class WatchListProduct(BaseModel):
    product_id: int
    region: Region
