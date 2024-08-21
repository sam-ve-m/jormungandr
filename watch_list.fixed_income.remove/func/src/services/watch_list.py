from func.src.domain.request.model import WatchListProduct
from func.src.domain.watch_list.model import WatchListProductModel
from func.src.repositories.watch_list.repository import WatchListRepository


class WatchListService:
    @classmethod
    async def delete_products(cls, watch_list_product: WatchListProduct, unique_id: str):
        product = WatchListProductModel(watch_list_product, unique_id)
        await WatchListRepository.remove_product_from_watch_list(product)
        return True
