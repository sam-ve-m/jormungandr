from unittest.mock import patch, MagicMock
from func.src.domain.models.employ_position.model import EmployPositionModel


dummy_value = 0, 1


@patch.object(EmployPositionModel, "__init__", return_value=None)
def test_from_database(mocked_instance):
    EmployPositionModel.from_database(dummy_value)
    mocked_instance.assert_called_once_with(
        code=dummy_value[0],
        value=dummy_value[1],
    )
