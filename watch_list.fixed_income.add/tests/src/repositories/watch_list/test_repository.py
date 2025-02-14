from unittest.mock import patch, AsyncMock

import pytest
from etria_logger import Gladsheim
from nidavellir import Sindri
from pytest import mark

from func.src.domain.request.model import WatchListProducts
from func.src.domain.watch_list.model import WatchListProductModel
from func.src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure
from func.src.repositories.watch_list.repository import WatchListRepository

dummy_products_to_insert = {
    "products": [
        {"product_id": 12, "region": "BR"},
        {"product_id": 13, "region": "US"},
        {"product_id": 14, "region": "BR"},
    ]
}

dummy_watch_list_products_model = [
    WatchListProductModel(product, "test_id")
    for product in WatchListProducts(**dummy_products_to_insert).products
]
dummy_insert = [
    str(Sindri.dict_to_primitive_types(x.to_dict()))
    for x in dummy_watch_list_products_model
]


@mark.asyncio
@patch.object(WatchListRepository, "_WatchListRepository__get_collection")
async def test_insert_all_products_in_watch_list(get_collection_mock, monkeypatch):
    class TransactionMock:
        async def __aenter__(self):
            return AsyncMock()

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            return

    class ActuallySessionMock:
        def start_transaction(self):
            return TransactionMock()

        async def __aenter__(self):
            return AsyncMock()

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    class SessionMock:
        session = ActuallySessionMock()

        async def __aenter__(self):
            return self.session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    class ClientMock:
        session = SessionMock()

        async def start_session(self):
            return self.session

        async def __aenter__(self):
            pass

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    def get_client_mock():
        return ClientMock()

    collection_mock = AsyncMock()
    collection_mock.update_one.return_value = True
    get_collection_mock.return_value = collection_mock

    monkeypatch.setattr(MongoDBInfrastructure, "get_client", get_client_mock)

    await WatchListRepository.insert_all_products_in_watch_list(
        dummy_watch_list_products_model
    )
    get_collection_mock.assert_called_once_with()
    assert collection_mock.update_one.call_count == len(dummy_watch_list_products_model)
    assert collection_mock.update_one.call_args_list[0].kwargs["upsert"] is True


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(WatchListRepository, "_WatchListRepository__get_collection")
async def test_insert_all_products_in_watch_list_exception(
    get_collection_mock, etria_error_mock, monkeypatch
):
    class ActuallySessionMock:
        def start_transaction(self):
            raise Exception("ERROR")

        async def __aenter__(self):
            return AsyncMock()

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    class SessionMock:
        session = ActuallySessionMock()

        async def __aenter__(self):
            return self.session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    class ClientMock:
        session = SessionMock()

        async def start_session(self):
            return self.session

        async def __aenter__(self):
            pass

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    def get_client_mock():
        return ClientMock()

    collection_mock = AsyncMock()
    collection_mock.update_one.return_value = True
    get_collection_mock.return_value = collection_mock

    monkeypatch.setattr(MongoDBInfrastructure, "get_client", get_client_mock)

    with pytest.raises(Exception):
        await WatchListRepository.insert_all_products_in_watch_list(
            dummy_watch_list_products_model
        )

        get_collection_mock.assert_called_once_with()
        get_collection_mock.assert_called_once_with()
        collection_mock.update_one.assert_not_called()
        collection_mock.update_one.assert_not_awaited()
        etria_error_mock.assert_called()
