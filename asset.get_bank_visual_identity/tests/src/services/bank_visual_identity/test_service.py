import pytest

from func.src.domain.exceptions.model import ImageNotFound
from func.src.domain.models.request.model import BankVisualIdentityModel
from func.src.repositories.bank_visual_identity.repository import (
    BankVisualIdentityRepository,
)
from func.src.repositories.cache.repository import CacheRepository
from func.src.services.bank_visual_identity.service import BankVisualIdentityService
from unittest.mock import patch
from pytest import mark

bank_code_model_dummy = BankVisualIdentityModel(bank_code=79, type="logo")


@mark.asyncio
@patch.object(BankVisualIdentityService, "_BankVisualIdentityService__get_logo_url")
async def test_get_bank_logo(get_url_mock):
    url_return_value = "https://www.image_link_here.com"
    get_url_mock.return_value = url_return_value
    result = await BankVisualIdentityService.get_bank_logo(bank_code_model_dummy)
    assert await get_url_mock.called_with(bank_code_model_dummy.bank_code)
    assert result == url_return_value


def test_get_logo_path(monkeypatch):
    monkeypatch.setattr(BankVisualIdentityService, "_BankVisualIdentityService__images_folder", "banks")
    expected_result = f"banks/79/logo.png"
    result = BankVisualIdentityService._BankVisualIdentityService__get_logo_path("79")
    assert result == expected_result


@mark.asyncio
@patch.object(
    BankVisualIdentityRepository,
    "generate_logo_url",
    return_value="https://www.image_link_here.com",
)
@patch.object(BankVisualIdentityRepository, "logo_exists", return_value=True)
@patch.object(
    CacheRepository, "get_cached_logo", return_value="https://www.image_link_here.com"
)
async def test_get_logo_url_when_there_is_cache(
    cache_mock, logo_exists_mock, generate_url_mock
):
    result = await BankVisualIdentityService._BankVisualIdentityService__get_logo_url(
        "79"
    )
    assert type(result) == str
    assert cache_mock.called
    assert not logo_exists_mock.called
    assert not generate_url_mock.called


@mark.asyncio
@patch.object(
    BankVisualIdentityRepository,
    "generate_logo_url",
    return_value="https://www.image_link_here.com",
)
@patch.object(BankVisualIdentityRepository, "logo_exists", return_value=True)
@patch.object(CacheRepository, "save_logo_in_cache", return_value=True)
@patch.object(CacheRepository, "get_cached_logo", return_value=None)
async def test_get_logo_url_when_there_is_no_cache_and_logo_exists(
    get_in_cache_mock, save_in_cache_mock, logo_exists_mock, generate_url_mock
):
    result = await BankVisualIdentityService._BankVisualIdentityService__get_logo_url(
        "79"
    )
    assert type(result) == str
    assert get_in_cache_mock.called
    assert save_in_cache_mock.called
    assert logo_exists_mock.called
    assert generate_url_mock.called


@mark.asyncio
@patch.object(
    BankVisualIdentityRepository,
    "generate_logo_url",
    return_value="https://www.image_link_here.com",
)
@patch.object(BankVisualIdentityRepository, "logo_exists", return_value=False)
@patch.object(CacheRepository, "get_cached_logo", return_value=None)
async def test_get_logo_url_when_there_is_no_cache_and_logo_does_not_exists(
    cache_mock, logo_exists_mock, generate_url_mock
):
    with pytest.raises(ImageNotFound):
        result = (
            await BankVisualIdentityService._BankVisualIdentityService__get_logo_url(
                "79"
            )
        )
    assert cache_mock.called
    assert logo_exists_mock.called
    assert not generate_url_mock.called
