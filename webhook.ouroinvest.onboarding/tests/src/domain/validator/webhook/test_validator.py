import pytest

from src.domain.enums.ouroinvest_status.enum import OuroInvestStatus
from src.domain.exceptions.exceptions import StatusSentIsNotValid
from src.domain.validator.webhook.validator import WebHookMessage


def test_status_validation():
    status = OuroInvestStatus._member_map_[OuroInvestStatus._member_names_[0]].value
    WebHookMessage(cpf="", status=status)
