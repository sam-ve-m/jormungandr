from unittest.mock import patch

from func.src.domain.models.employ_type.model import EmployTypeModel
from func.src.repositories.cache.repository import EmployTypeCacheRepository
from func.src.repositories.oracle.repository import EmployTypeOracleRepository
from func.src.services.employ_type.service import EmployTypeService


@patch.object(EmployTypeCacheRepository, "get_employ_type_enum")
@patch.object(EmployTypeOracleRepository, "get_employ_type")
@patch.object(EmployTypeCacheRepository, "save_employ_type_enum")
@patch.object(EmployTypeModel, "from_database")
def test_get_employ_type_response(
        mocked_model,
        mocked_save,
        mocked_get_new,
        mocked_get
):
    mocked_get.return_value = [123]
    response = EmployTypeService.get_employ_type_response()
    mocked_get.assert_called_once()
    mocked_save.assert_not_called()
    mocked_model.assert_called_once()
    mocked_get_new.assert_not_called()
    assert response == [mocked_model.return_value]


@patch.object(EmployTypeCacheRepository, "get_employ_type_enum")
@patch.object(EmployTypeOracleRepository, "get_employ_type")
@patch.object(EmployTypeCacheRepository, "save_employ_type_enum")
@patch.object(EmployTypeModel, "from_database")
def test_get_employ_type_response_create_new(
        mocked_model,
        mocked_save,
        mocked_get_new,
        mocked_get
):
    mocked_get.return_value = None
    mocked_get_new.return_value = [123]
    response = EmployTypeService.get_employ_type_response()
    mocked_get.assert_called_once()
    mocked_model.assert_called_once()
    mocked_get_new.assert_called_once()
    mocked_save.assert_called_once_with(mocked_get_new.return_value)
    assert response == [mocked_model.return_value]
