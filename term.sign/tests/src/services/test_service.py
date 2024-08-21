from func.src.domain.exceptions.exceptions import (
    UserUniqueIdNotExists,
    TermVersionNotExists,
    ErrorOnUpdateUser,
)
from .stubs import (
    stub_unique_id,
    stub_user_not_updated,
    stub_user_updated,
    stub_terms_model,
)

# Standards
from unittest.mock import patch

# Third party
import pytest


@pytest.mark.asyncio
@patch("func.src.services.terms.UserRepository.find_one_by_unique_id", return_value=True)
async def test_when_unique_id_exists_then_proceed(mock_find_one, term_sign_service):
    success = await term_sign_service._verify_unique_id_exists()

    assert success is True
    mock_find_one.assert_called_once_with(unique_id=stub_unique_id)


@pytest.mark.asyncio
@patch("func.src.services.terms.UserRepository.find_one_by_unique_id", return_value=None)
async def test_when_unique_id_not_exists_then_raises(mock_find_one, term_sign_service):
    with pytest.raises(UserUniqueIdNotExists):
        await term_sign_service._verify_unique_id_exists()


@pytest.mark.asyncio
@patch(
    "func.src.services.terms.FileRepository.get_current_term_version",
    side_effect=[1, 5, 3],
)
async def test_when_success_to_find_terms_version_then_return_terms_version(
    mock_get_term_version, term_sign_service
):
    terms_version = await term_sign_service._get_terms_version()

    assert isinstance(terms_version, list)
    assert terms_version[0] == 1
    assert terms_version[1] == 5
    assert terms_version[2] == 3


@pytest.mark.asyncio
@patch(
    "func.src.services.terms.FileRepository.get_current_term_version",
    side_effect=[1, 5, 3],
)
async def test_when_success_to_find_terms_version_then_mock_was_called(
    mock_get_term_version, term_sign_service
):
    await term_sign_service._get_terms_version()

    assert mock_get_term_version.call_count == 3


@pytest.mark.asyncio
@patch(
    "func.src.services.terms.FileRepository.get_current_term_version",
    side_effect=[1, 0, 3],
)
async def test_when_not_find_terms_version_then_raises(
    mock_get_term_version, term_sign_service
):
    with pytest.raises(TermVersionNotExists):
        await term_sign_service._get_terms_version()


@pytest.mark.asyncio
@patch(
    "func.src.services.terms.UserRepository.update_one_with_terms_signed",
    return_value=stub_user_updated,
)
@patch("func.src.services.terms.Audit.record_message_log")
@patch(
    "func.src.services.terms.FileRepository.get_current_term_version",
    side_effect=[1, 5, 3],
)
async def test_when_user_terms_sign_success_then_return_true(
    mock_term_version, mock_audit, mock_user_update, term_sign_service
):
    success = await term_sign_service.user_terms_sign()

    assert success is True


@pytest.mark.asyncio
@patch(
    "func.src.services.terms.UserRepository.update_one_with_terms_signed",
    return_value=stub_user_updated,
)
@patch("func.src.services.terms.Audit.record_message_log")
@patch(
    "func.src.services.terms.FileRepository.get_current_term_version",
    side_effect=[1, 5, 3],
)
async def test_when_user_terms_sign_success_then_mocks_was_called(
    mock_term_version, mock_audit, mock_user_update, term_sign_service
):
    await term_sign_service.user_terms_sign()

    mock_term_version.assert_called()
    mock_audit.assert_called_once()
    mock_user_update.assert_called_once()


@pytest.mark.asyncio
@patch(
    "func.src.services.terms.UserRepository.update_one_with_terms_signed",
    return_value=stub_user_not_updated,
)
@patch("func.src.services.terms.Audit.record_message_log")
@patch(
    "func.src.services.terms.FileRepository.get_current_term_version",
    side_effect=[1, 5, 3],
)
async def test_when_failed_to_update_user_terms_sign_then_raises(
    mock_term_version, mock_audit, mock_user_update, term_sign_service
):
    with pytest.raises(ErrorOnUpdateUser):
        await term_sign_service.user_terms_sign()
