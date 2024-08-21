from unittest.mock import patch, MagicMock, AsyncMock

import orjson
import pytest
from decouple import Config
from etria_logger import Gladsheim

from func.src.domain.exceptions.exceptions import CityEnumNotFound, StateEnumNotFound, ErrorRequestingEnum
from func.src.infrastructure.http.infrastructure import HttpInfrastructure
from func.src.domain.validator.address import AddressEnum
from func.src.transport.enums import JormungandrEnums


dummy_value = MagicMock()


@pytest.mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(HttpInfrastructure, "get_session")
@patch.object(orjson, "loads")
async def test_request(
        mocked_parse,
        mocked_infra,
        mocked_logger
):
    mocked_infra.return_value = AsyncMock()
    mocked_infra.return_value.get.return_value.status = 200
    response = await JormungandrEnums._request(dummy_value, dummy_value)
    mocked_infra.return_value.get.assert_called_once_with(dummy_value, params=dummy_value)
    mocked_parse.assert_called_once_with(
        mocked_infra.return_value.get.return_value.text.return_value
    )
    assert response == mocked_parse.return_value.get.return_value
    mocked_logger.assert_not_called()


@pytest.mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(HttpInfrastructure, "get_session")
@patch.object(orjson, "loads")
async def test_request_raising(
        mocked_parse,
        mocked_infra,
        mocked_logger
):
    mocked_infra.return_value = AsyncMock()
    mocked_infra.return_value.get.return_value.status = 500
    with pytest.raises(ErrorRequestingEnum):
        await JormungandrEnums._request(dummy_value, dummy_value)
    mocked_infra.return_value.get.assert_called_once_with(dummy_value, params=dummy_value)
    mocked_logger.assert_called_once_with(
        message="Unable to get enum", content=mocked_infra.return_value.get.return_value.text.return_value
    )
    mocked_parse.assert_not_called()


@pytest.mark.asyncio
@patch.object(Config, "__call__")
@patch.object(JormungandrEnums, "_request")
@patch.object(AddressEnum, "__init__", return_value=None)
@patch.object(Gladsheim, "error")
async def test_find_city_enum_code(
        mocked_logger,
        mocked_model,
        mocked_request,
        mocked_env
):
    city = MagicMock()
    mocked_request.return_value = [city]
    city.__getitem__.return_value = dummy_value.upper.return_value
    await JormungandrEnums.find_city_enum_code(dummy_value, dummy_value)
    mocked_request.assert_called_once_with(mocked_env.return_value, {
        "country": mocked_env.return_value,
        "state": dummy_value,
    })
    mocked_model.assert_called_once_with(
        value=dummy_value,
        code=city.__getitem__.return_value,
    )
    mocked_logger.assert_not_called()


@pytest.mark.asyncio
@patch.object(Config, "__call__")
@patch.object(JormungandrEnums, "_request")
@patch.object(AddressEnum, "__init__", return_value=None)
@patch.object(Gladsheim, "error")
async def test_find_city_enum_code_raising(
        mocked_logger,
        mocked_model,
        mocked_request,
        mocked_env
):
    city = MagicMock()
    mocked_request.return_value = [city]
    with pytest.raises(CityEnumNotFound):
        await JormungandrEnums.find_city_enum_code(dummy_value, dummy_value)
    mocked_request.assert_called_once_with(mocked_env.return_value, {
        "country": mocked_env.return_value,
        "state": dummy_value,
    })

    mocked_logger.assert_called_once_with(
        message="Unable to find city", city=dummy_value
    )
    mocked_model.assert_not_called()


@pytest.mark.asyncio
@patch.object(Config, "__call__")
@patch.object(JormungandrEnums, "_request")
@patch.object(AddressEnum, "__init__", return_value=None)
@patch.object(Gladsheim, "error")
async def test_find_state_enum_code(
        mocked_logger,
        mocked_model,
        mocked_request,
        mocked_env
):

    state = MagicMock()
    mocked_request.return_value = [state]
    state.__getitem__.return_value = dummy_value
    await JormungandrEnums.find_state_enum_code(dummy_value)
    mocked_request.assert_called_once_with(mocked_env.return_value, {
        "country": mocked_env.return_value,
    })
    mocked_model.assert_called_once_with(
        value=state.__getitem__.return_value,
        code=dummy_value,
    )
    mocked_logger.assert_not_called()


@pytest.mark.asyncio
@patch.object(Config, "__call__")
@patch.object(JormungandrEnums, "_request")
@patch.object(AddressEnum, "__init__", return_value=None)
@patch.object(Gladsheim, "error")
async def test_find_state_enum_code_raising(
        mocked_logger,
        mocked_model,
        mocked_request,
        mocked_env
):

    state = MagicMock()
    mocked_request.return_value = [state]
    with pytest.raises(StateEnumNotFound):
        await JormungandrEnums.find_state_enum_code(dummy_value)
    mocked_request.assert_called_once_with(mocked_env.return_value, {
        "country": mocked_env.return_value,
    })
    mocked_logger.assert_called_once_with(
        message="Unable to find state", state=dummy_value
    )
    mocked_model.assert_not_called()
