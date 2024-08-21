from func.src.domain.request.model import WatchListProduct


class WatchListProductModel:
    def __init__(self, watch_list_product: WatchListProduct, unique_id: str):
        self.__unique_id = unique_id
        self.__product_id = watch_list_product.product_id
        self.__region = watch_list_product.region

    def get_id(self) -> str:
        _id = f"{self.__product_id}_{self.__region.value}_{self.__unique_id}"
        return _id
