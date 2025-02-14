from unittest.mock import patch

from decouple import Config
import pytest

from func.src.domain.exceptions.exceptions import OnboardingStepsStatusCodeNotOk
from func.src.transports.onboarding_steps.transport import OnboardingSteps
from tests.src.transports.onboarding.stubs import (
    stub_request_success,
    stub_request_failure,
)


@pytest.mark.asyncio
@patch.object(Config, "__call__")
@patch(
    "func.src.transports.onboarding_steps.transport.AsyncClient.get",
    return_value=stub_request_success,
)
async def test_when_success_to_get_onboarding_steps_then_returns_current_step(
    mock_httpx_client, config_mock
):
    user_current_step = await OnboardingSteps.get_user_current_step(jwt="12345")

    assert isinstance(user_current_step, str)
    assert user_current_step == "selfie"


@pytest.mark.asyncio
@patch.object(Config, "__call__")
@patch(
    "func.src.transports.onboarding_steps.transport.AsyncClient.get",
    return_value=stub_request_failure,
)
async def test_when_failure_to_get_onboarding_steps_then_raises(
    mock_httpx_client, config_mock
):
    with pytest.raises(OnboardingStepsStatusCodeNotOk):
        await OnboardingSteps.get_user_current_step(jwt="12345")
