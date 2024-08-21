from typing import List
from unittest.mock import patch, MagicMock

from func.src.infrastructure.oracle.infrastructure import OracleInfrastructure
from func.src.repositories.oracle.repository import EmployStatusOracleRepository


@patch.object(EmployStatusOracleRepository, "_query")
def test_get_employ_status(mocked_query):
    response = EmployStatusOracleRepository.get_employ_status()
    mocked_query.assert_called_once()
    assert response == mocked_query.return_value


dummy_value = MagicMock()


@patch.object(EmployStatusOracleRepository, "_normalize_encode")
@patch.object(OracleInfrastructure, "get_cursor")
def test_query(mocked_infra, mocked_parser):
    result = EmployStatusOracleRepository._query(dummy_value)
    mocked_infra.assert_called_once_with()
    mocked_infra.return_value.__enter__.return_value.execute.assert_called_once_with(
        dummy_value
    )
    mocked_parser.assert_called_once_with(
        rows=mocked_infra.return_value.__enter__.return_value.fetchall.return_value
    )
    assert result == mocked_parser.return_value


def test_normalize_encode():
    result = EmployStatusOracleRepository._normalize_encode([
        (1, 1, 1),
        (1, 'お可愛いこと', 1),
    ])
    assert result == [
        (1, 1, 1),
        (1, 'お可愛いこと', 1),
    ]