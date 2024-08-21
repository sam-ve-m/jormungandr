from unittest.mock import MagicMock

import pytest

from func.src.domain.enums.bureau.enum import BureauType, BureauStatus
from func.src.domain.validator.webhook.validator import WebHookMessage
from func.src.domain.exceptions.exceptions import InvalidMessageTypeReceived, InvalidStatusReceived


stub_request_body = MagicMock()


def test_status_validation_raising_type():
    stub_request_body.get.side_effect = [
        None,
        BureauType._member_map_[BureauType._member_names_[0]].value+"asd",
        BureauStatus._member_map_[BureauStatus._member_names_[0]].value,
    ]
    with pytest.raises(InvalidMessageTypeReceived):
        WebHookMessage.from_request(stub_request_body)


def test_status_validation_raising_status():
    stub_request_body.get.side_effect = [
        None,
        BureauType._member_names_[0],
        BureauStatus._member_map_[BureauStatus._member_names_[0]].value,
    ]
    with pytest.raises(InvalidStatusReceived):
        WebHookMessage.from_request(stub_request_body)


def test_status_validation():
    stub_request_body.get.side_effect = [
        None,
        BureauType._member_names_[0],
        BureauStatus._member_names_[0],
        None, None, None, None,
    ]
    WebHookMessage.from_request(stub_request_body)
