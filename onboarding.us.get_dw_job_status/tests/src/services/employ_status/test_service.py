from unittest.mock import patch

from func.src.domain.models.employ_status.model import EmployStatusModel
from func.src.repositories.cache.repository import EmployStatusCacheRepository
from func.src.repositories.oracle.repository import EmployStatusOracleRepository
from func.src.services.employ_status.service import EmployStatusService


@patch.object(EmployStatusCacheRepository, "get_employ_status_enum")
@patch.object(EmployStatusOracleRepository, "get_employ_status")
@patch.object(EmployStatusCacheRepository, "save_employ_status_enum")
@patch.object(EmployStatusModel, "from_database")
def test_get_employ_status_response(
        mocked_model,
        mocked_save,
        mocked_get_new,
        mocked_get
):
    mocked_get.return_value = [123]
    response = EmployStatusService.get_employ_status_response()
    mocked_get.assert_called_once()
    mocked_save.assert_not_called()
    mocked_model.assert_called_once()
    mocked_get_new.assert_not_called()
    assert response == [mocked_model.return_value]


@patch.object(EmployStatusCacheRepository, "get_employ_status_enum")
@patch.object(EmployStatusOracleRepository, "get_employ_status")
@patch.object(EmployStatusCacheRepository, "save_employ_status_enum")
@patch.object(EmployStatusModel, "from_database")
def test_get_employ_status_response_create_new(
        mocked_model,
        mocked_save,
        mocked_get_new,
        mocked_get
):
    mocked_get.return_value = None
    mocked_get_new.return_value = [123]
    response = EmployStatusService.get_employ_status_response()
    mocked_get.assert_called_once()
    mocked_model.assert_called_once()
    mocked_get_new.assert_called_once()
    mocked_save.assert_called_once_with(mocked_get_new.return_value)
    assert response == [mocked_model.return_value]
