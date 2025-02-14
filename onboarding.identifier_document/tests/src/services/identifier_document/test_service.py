# Jormungandr
from func.src.domain.exceptions.exceptions import (
    FileNotExists,
    InvalidOnboardingCurrentStep,
)
from .stubs import stub_content
from .image import image_b64

# Standards
from unittest.mock import patch
from io import BufferedRandom

# Third party
import pytest


@pytest.mark.asyncio
@patch(
    "func.src.services.identifier_document.FileRepository.list_contents",
    return_value=stub_content,
)
async def test_when_content_exists_then_return_true(
    mock_list_contents, document_service
):
    result = await document_service._content_exists()

    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.services.identifier_document.FileRepository.list_contents",
    return_value=stub_content,
)
async def test_when_content_exists_then_mock_was_called(
    mock_list_contents, document_service
):
    await document_service._content_exists()

    mock_list_contents.assert_called()
    assert mock_list_contents.call_count == 2


@pytest.mark.asyncio
@patch(
    "func.src.services.identifier_document.FileRepository.list_contents",
    return_value=None,
)
async def test_when_content_not_exists_then_raises(
    mock_list_contents, document_service
):
    with pytest.raises(FileNotExists):
        await document_service._content_exists()


@pytest.mark.asyncio
async def test_when_decode_document_then_return_temp_file(document_service):
    temp_file = await document_service._resolve_content(document=image_b64)

    assert isinstance(temp_file, BufferedRandom)


@pytest.mark.asyncio
@patch("func.src.services.identifier_document.Audit.record_message_log")
@patch(
    "func.src.services.identifier_document.FileRepository.list_contents",
    return_value=stub_content,
)
@patch("func.src.services.identifier_document.FileRepository.save_user_document_file")
async def test_when_valid_document_then_return_true(
    mock_save_document, mock_list_contents, mock_audit, document_service
):
    success = await document_service.save_user_document_file()

    assert success is True


@pytest.mark.asyncio
@patch(
    "func.src.services.identifier_document.OnboardingSteps._get_user_current_step",
    return_value="document_validator",
)
async def test_when_current_step_correct_then_return_true(
    mock_onboarding_steps, document_service
):
    result = await document_service.validate_current_onboarding_step(jwt="123")

    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.services.identifier_document.OnboardingSteps._get_user_current_step",
    side_effect=["finished", "user_document_validator"],
)
async def test_when_current_step_correct_then_return_true_us(
    mock_onboarding_steps, document_service
):
    result = await document_service.validate_current_onboarding_step(jwt="123")

    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.services.identifier_document.OnboardingSteps._get_user_current_step",
    return_value="finished",
)
async def test_when_current_step_invalid_then_return_raises_us(
    mock_onboarding_steps, document_service
):
    with pytest.raises(InvalidOnboardingCurrentStep):
        await document_service.validate_current_onboarding_step(jwt="123")


@pytest.mark.asyncio
@patch(
    "func.src.services.identifier_document.OnboardingSteps._get_user_current_step",
    return_value="other",
)
async def test_when_current_step_invalid_then_return_raises(
    mock_onboarding_steps, document_service
):
    with pytest.raises(InvalidOnboardingCurrentStep):
        await document_service.validate_current_onboarding_step(jwt="123")
