from typing import List, Optional
from unittest.mock import patch, MagicMock

import pytest
from etria_logger import Gladsheim
from mnemosine import SyncCache

from func.src.domain.exceptions.exceptions import FailToFetchData
from func.src.repositories.cache.repository import EmployPositionCacheRepository


dummy_value, dummy_exception = MagicMock(), Exception()


@patch.object(SyncCache, "save")
@patch.object(Gladsheim, "error")
def test_save_employ_position_enum(mocked_logger, mocked_save, monkeypatch):
    monkeypatch.setattr(EmployPositionCacheRepository, "enum_key", dummy_value)
    result = EmployPositionCacheRepository.save_employ_position_enum([1,2,3], dummy_value)
    mocked_save.assert_called_once_with(dummy_value, [1,2,3], dummy_value)
    mocked_logger.assert_not_called()
    assert result is True


@patch.object(SyncCache, "save", side_effect=dummy_exception)
@patch.object(Gladsheim, "error")
def test_save_employ_position_enum_raising(mocked_logger, mocked_save, monkeypatch):
    monkeypatch.setattr(EmployPositionCacheRepository, "enum_key", dummy_value)
    with pytest.raises(FailToFetchData):
        EmployPositionCacheRepository.save_employ_position_enum([1, 2, 3], dummy_value)
    mocked_save.assert_called_once_with(dummy_value, [1, 2, 3], dummy_value)
    mocked_logger.assert_called_once_with(
        error=dummy_exception, message="Error saving enum in cache."
    )


@patch.object(SyncCache, "get")
@patch.object(Gladsheim, "error")
def test_get_employ_position_enum(mocked_logger, mocked_get, monkeypatch):
    monkeypatch.setattr(EmployPositionCacheRepository, "enum_key", dummy_value)
    result = EmployPositionCacheRepository.get_employ_position_enum()
    mocked_get.assert_called_once_with(dummy_value)
    mocked_logger.assert_not_called()
    assert result == mocked_get.return_value


@patch.object(SyncCache, "get", side_effect=dummy_exception)
@patch.object(Gladsheim, "error")
def test_get_employ_position_enum_raising(mocked_logger, mocked_get, monkeypatch):
    monkeypatch.setattr(EmployPositionCacheRepository, "enum_key", dummy_value)
    with pytest.raises(FailToFetchData):
        EmployPositionCacheRepository.get_employ_position_enum()
    mocked_get.assert_called_once_with(dummy_value)
    mocked_logger.assert_called_once_with(
        error=dummy_exception, message="Error saving enum in cache."
    )
