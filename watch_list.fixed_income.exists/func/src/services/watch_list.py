from func.src.domain.request.model import WatchListProduct
from func.src.domain.watch_list.model import WatchListProductModel
from func.src.repositories.watch_list.repository import WatchListRepository


class WatchListService:
    @classmethod
    async def product_exists(cls, watch_list_product: WatchListProduct, unique_id: str):
        product = WatchListProductModel(watch_list_product, unique_id)
        exists = await WatchListRepository.exists(product)

        service_result = {"is_product_in_watchlist": exists}

        return service_result
