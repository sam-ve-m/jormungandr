import os
from unittest.mock import patch

import pytest

env_mock = {
    "QUESTION_FIRST_ID": "1",
    "ANSWER_FIRST_ID": "1",
    "QUESTION_FINAL_ID": "8",
    "ANSWER_FINAL_ID": "4",
    "FIRST_PROFILE_RANGE": "0.5680",
    "SECOND_PROFILE_RANGE": "0.6399",
    "THIRD_PROFILE_RANGE": "0.7899",
    "FOURTH_PROFILE_RANGE": "1.0000",
}

with patch.dict(os.environ, env_mock):
    from func.src.domain.exceptions.transports.exception import ErrorOnSendAuditLog
    from func.src.transports.audit.transport import Audit
    from tests.src.services.suitability.stubs import stub_suitability_model


@pytest.mark.asyncio
@patch(
    "func.src.transports.audit.transport.Persephone.send_to_persephone",
    return_value=(1, 0),
)
@patch("func.src.transports.audit.transport.config")
async def test_when_success_to_record_message_then_return_true(
    mock_config, mock_persephone
):
    result = await Audit.record_message_log(suitability_model=stub_suitability_model)

    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.transports.audit.transport.Persephone.send_to_persephone",
    return_value=(0, 0),
)
@patch("func.src.transports.audit.transport.config")
async def test_when_fail_to_record_message_then_raises(mock_config, mock_persephone):
    with pytest.raises(ErrorOnSendAuditLog):
        await Audit.record_message_log(suitability_model=stub_suitability_model)
