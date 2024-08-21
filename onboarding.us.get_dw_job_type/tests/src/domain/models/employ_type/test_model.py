from unittest.mock import patch, MagicMock
from func.src.domain.models.employ_type.model import EmployTypeModel


dummy_value = 0, 1


@patch.object(EmployTypeModel, "__init__", return_value=None)
def test_from_database(mocked_instance):
    EmployTypeModel.from_database(dummy_value)
    mocked_instance.assert_called_once_with(
        code=dummy_value[0],
        value=dummy_value[1],
    )
