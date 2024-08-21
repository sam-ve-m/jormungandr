from unittest.mock import patch

from pytest import mark

from func.src.domain.request.model import WatchListProduct
from func.src.domain.watch_list.model import WatchListProductModel
from func.src.repositories.watch_list.repository import WatchListRepository
from func.src.services.watch_list import WatchListService

dummy_products_to_register = {"product_id": 12, "region": "BR"}
dummy_watch_list_products = WatchListProduct(**dummy_products_to_register)


@mark.asyncio
@patch.object(WatchListRepository, "remove_product_from_watch_list")
async def test_register_products(remove_products_from_watch_list_mock):
    result = await WatchListService.delete_products(dummy_watch_list_products, "test-id")
    assert remove_products_from_watch_list_mock.call_count == 1
    for call in remove_products_from_watch_list_mock.call_args[0]:
        assert isinstance(call, WatchListProductModel)
    assert result is True
