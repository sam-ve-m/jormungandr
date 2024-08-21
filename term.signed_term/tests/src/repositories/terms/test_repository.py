from unittest.mock import patch

from pytest import mark

from func.src.domain.enums.terms import TermsFileType
from func.src.infrastructures.s3.s3 import S3Infrastructure
from func.src.repositories.terms.repository import (
    TermRepository,
)

bucket_name_dummy = "__bucket_name"
folder_path_dummy = "term_refusal/"
item_key_dummy = "key"
link_dummy = "www.link.com.br"


class GetClientMock:
    async def __aenter__(self):
        class Client:
            async def generate_presigned_url(self, *args, **kwargs):
                return link_dummy

        return Client()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return


def test___resolve_term_path():
    term_dummy = TermsFileType.TERM_REFUSAL
    result = TermRepository._TermRepository__resolve_term_path(term_dummy)
    expected_result = "term_refusal/"
    assert result == expected_result


def test___generate_term_file_name():
    result = TermRepository._TermRepository__generate_term_file_name(
        "term_refusal", "4"
    )
    expected_result = "term_refusal_v4"
    assert result == expected_result


def test___get_file_extension_by_type():
    term_dummy = TermsFileType.TERM_REFUSAL
    result = TermRepository._TermRepository__get_file_extension_by_type(term_dummy)
    expected_result = ".pdf"
    assert result == expected_result


@mark.asyncio
async def test__generate_term_url(monkeypatch):
    monkeypatch.setattr(S3Infrastructure, "get_client", GetClientMock)
    result = await TermRepository._generate_term_url(
        term_path="", file_name="", file_extension=""
    )
    expected_result = link_dummy
    assert result == expected_result


@mark.asyncio
@patch.object(
    TermRepository, "_TermRepository__generate_term_file_name", return_value=""
)
@patch.object(TermRepository, "_TermRepository__resolve_term_path", return_value="")
@patch.object(
    TermRepository, "_TermRepository__get_file_extension_by_type", return_value=""
)
@patch.object(TermRepository, "_generate_term_url")
async def test_get_term_link_by_version(
    generate_term_mock,
    get_file_extension_mock,
    resolve_path_mock,
    generate_file_name_mock,
):
    term_dummy = TermsFileType.TERM_REFUSAL
    generate_term_mock.return_value = link_dummy
    result = await TermRepository.get_term_link_by_version(term_dummy, "4")
    expected_result = link_dummy
    assert result == expected_result
    assert generate_term_mock.called
    assert get_file_extension_mock.called
    assert resolve_path_mock.called
    assert generate_file_name_mock.called
