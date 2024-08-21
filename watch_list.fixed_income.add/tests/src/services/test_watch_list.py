from unittest.mock import patch

from pytest import mark

from func.src.domain.request.model import WatchListProducts
from func.src.domain.watch_list.model import WatchListProductModel
from func.src.repositories.watch_list.repository import WatchListRepository
from func.src.services.watch_list import WatchListService

dummy_products_to_register = {
    "products": [
        {"product_id": 12, "region": "BR"},
        {"product_id": 13, "region": "US"},
        {"product_id": 14, "region": "BR"},
    ]
}

dummy_watch_list_products = WatchListProducts(**dummy_products_to_register)


@mark.asyncio
@patch.object(WatchListRepository, "insert_all_products_in_watch_list")
async def test_register_products(insert_all_products_in_watch_list_mock):
    result = await WatchListService.register_products(
        dummy_watch_list_products, "test-id"
    )
    assert insert_all_products_in_watch_list_mock.call_count == 1
    for call in insert_all_products_in_watch_list_mock.call_args[0][0]:
        assert isinstance(call, WatchListProductModel)
    assert result is True
