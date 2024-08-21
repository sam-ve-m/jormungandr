from unittest.mock import patch

from func.src.domain.models.employ_position.model import EmployPositionModel
from func.src.repositories.cache.repository import EmployPositionCacheRepository
from func.src.repositories.oracle.repository import EmployPositionOracleRepository
from func.src.services.employ_position.service import EmployPositionService


@patch.object(EmployPositionCacheRepository, "get_employ_position_enum")
@patch.object(EmployPositionOracleRepository, "get_employ_position")
@patch.object(EmployPositionCacheRepository, "save_employ_position_enum")
@patch.object(EmployPositionModel, "from_database")
def test_get_employ_position_response(
        mocked_model,
        mocked_save,
        mocked_get_new,
        mocked_get
):
    mocked_get.return_value = [123]
    response = EmployPositionService.get_employ_position_response()
    mocked_get.assert_called_once()
    mocked_save.assert_not_called()
    mocked_model.assert_called_once()
    mocked_get_new.assert_not_called()
    assert response == [mocked_model.return_value]


@patch.object(EmployPositionCacheRepository, "get_employ_position_enum")
@patch.object(EmployPositionOracleRepository, "get_employ_position")
@patch.object(EmployPositionCacheRepository, "save_employ_position_enum")
@patch.object(EmployPositionModel, "from_database")
def test_get_employ_position_response_create_new(
        mocked_model,
        mocked_save,
        mocked_get_new,
        mocked_get
):
    mocked_get.return_value = None
    mocked_get_new.return_value = [123]
    response = EmployPositionService.get_employ_position_response()
    mocked_get.assert_called_once()
    mocked_model.assert_called_once()
    mocked_get_new.assert_called_once()
    mocked_save.assert_called_once_with(mocked_get_new.return_value)
    assert response == [mocked_model.return_value]
