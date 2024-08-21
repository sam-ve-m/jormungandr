import pytest
from etria_logger import Gladsheim

from func.src.domain.exceptions.model import FileNotFound, TermNotSigned
from func.src.domain.models.request.model import TermModel
from func.src.repositories.terms.repository import (
    TermRepository,
)
from func.src.repositories.user.repository import UserRepository
from func.src.services.terms.service import TermService
from unittest.mock import patch
from pytest import mark

term_model_dummy = TermModel(file_type="term_refusal")
term_model_not_signed_dummy = TermModel(file_type="term_application")
link_dummy = "https://www.term_link_here.com"
user_document_dummy = {"terms": {"term_refusal": {"version": 4}}}


@mark.asyncio
@patch.object(
    TermRepository,
    "get_term_link_by_version",
    return_value=link_dummy,
)
@patch.object(TermService, "_TermService__get_user_term_version", return_value="4")
async def test_get_user_signed_term_url(get_user_mock, get_term_link_mock):
    result = await TermService.get_user_signed_term_url(term_model_dummy, "unique-id")
    assert get_user_mock.called
    assert get_term_link_mock.called
    assert result == link_dummy


@mark.asyncio
@patch.object(
    UserRepository,
    "find_user",
    return_value=user_document_dummy,
)
async def test___get_user_term_version(find_user_mock):
    result = await TermService._TermService__get_user_term_version(
        term_model_dummy, "unique-id"
    )
    assert find_user_mock.called
    assert result == 4


@mark.asyncio
@patch.object(
    Gladsheim,
    "error",
)
@patch.object(
    UserRepository,
    "find_user",
    return_value=user_document_dummy,
)
async def test___get_user_term_version_when_term_is_not_signed(
    find_user_mock, etria_mock
):
    with pytest.raises(TermNotSigned):
        result = await TermService._TermService__get_user_term_version(
            term_model_not_signed_dummy, "unique-id"
        )
    assert find_user_mock.called
    assert etria_mock.called
