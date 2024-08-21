from unittest.mock import patch, AsyncMock, MagicMock

import pytest
from pytest import mark

from src.domain.enums.terms.enum import TermsFileType
from src.domain.exceptions.exceptions import FileNotFound
from src.infrastructures.s3.s3 import S3Infrastructure
from src.repositories.terms.repository import (
    TermRepository,
)

bucket_name_dummy = "bucket_name"
folder_path_dummy = "term_refusal/"
item_key_dummy = "key"
link_dummy = "www.link.com.br"


class FilterMock:
    iteration_return = "document"
    iteration = 0

    def __aiter__(self):
        return self

    def __anext__(self):
        if self.iteration > 1:
            raise StopAsyncIteration
        else:
            self.iteration += 1

            async def get_item():
                item = MagicMock()
                item.key = item_key_dummy
                item.meta.data.get.return_value = 1
                return item

            return get_item()


class InfraMock:
    async def __aenter__(self):
        class Object(AsyncMock):
            def filter(self, Prefix=None, Delimiter=None):
                filter_mock = FilterMock()
                return filter_mock

        class Bucket_:
            async def __call__(self, *args, **kwargs):
                return Bucket_()

            objects = Object()

        class GetResource:
            Bucket = Bucket_()

        return GetResource()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return


class GetClientMock:
    async def __aenter__(self):
        class Client:
            async def generate_presigned_url(self, *args, **kwargs):
                return link_dummy

        return Client()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return


@mark.asyncio
async def test__get_last_saved_file_from_folder_when_files_exist(monkeypatch):
    monkeypatch.setattr(S3Infrastructure, "get_resource", InfraMock)
    result = await TermRepository._get_last_saved_file_from_folder(
        folder_path=folder_path_dummy,
        bucket_name=bucket_name_dummy,
    )
    expected_result = item_key_dummy
    assert result == expected_result


@mark.asyncio
async def test__get_last_saved_file_from_folder_when_files_do_not_exist(monkeypatch):
    monkeypatch.setattr(FilterMock, "iteration", 2)
    monkeypatch.setattr(S3Infrastructure, "get_resource", InfraMock)
    with pytest.raises(FileNotFound):
        result = await TermRepository._get_last_saved_file_from_folder(
            folder_path=folder_path_dummy,
            bucket_name=bucket_name_dummy,
        )


def test__resolve_term_path():
    term_dummy = TermsFileType.TERM_REFUSAL
    result = TermRepository._resolve_term_path(term_dummy)
    expected_result = "term_refusal/"
    assert result == expected_result


@mark.asyncio
async def test__generate_term_url(monkeypatch):
    monkeypatch.setattr(S3Infrastructure, "get_client", GetClientMock)
    result = await TermRepository._generate_term_url(term_path="path")
    expected_result = link_dummy
    assert result == expected_result


@mark.asyncio
@patch.object(TermRepository, "_generate_term_url")
@patch.object(TermRepository, "_get_last_saved_file_from_folder")
async def test_get_term_link(last_saved_file_mock, generate_term_mock):
    term_dummy = TermsFileType.TERM_REFUSAL
    term_path_dummy = "term_refusal/term"
    last_saved_file_mock.return_value = term_path_dummy
    generate_term_mock.return_value = link_dummy
    result = await TermRepository.get_term_link(term_dummy)
    expected_result = link_dummy
    assert result == expected_result
    assert await generate_term_mock.called_with(term_path_dummy)
