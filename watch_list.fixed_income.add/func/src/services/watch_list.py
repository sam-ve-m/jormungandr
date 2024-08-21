from func.src.domain.request.model import WatchListProducts
from func.src.domain.watch_list.model import WatchListProductModel
from func.src.repositories.watch_list.repository import WatchListRepository


class WatchListService:
    @classmethod
    async def register_products(
        cls, watch_list_products: WatchListProducts, unique_id: str
    ):
        products_list = [
            WatchListProductModel(product, unique_id)
            for product in watch_list_products.products
        ]
        await WatchListRepository.insert_all_products_in_watch_list(products_list)
        return True
