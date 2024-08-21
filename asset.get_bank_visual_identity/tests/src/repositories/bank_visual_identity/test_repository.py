from unittest.mock import patch, AsyncMock, MagicMock

from pytest import mark

from func.src.infrastructures.s3.s3 import S3Infrastructure
from func.src.repositories.bank_visual_identity.repository import (
    BankVisualIdentityRepository,
)


@mark.asyncio
@patch.object(S3Infrastructure, "get_bucket")
async def test_logo_exists(get_bucker_mock):
    bucket_mock = MagicMock()
    bucket_mock.objects.filter.return_value = ["content"]
    get_bucker_mock.return_value = bucket_mock
    result = await BankVisualIdentityRepository.logo_exists("/file_path")
    assert bucket_mock.objects.filter.called
    assert type(result) == bool


@mark.asyncio
@patch.object(S3Infrastructure, "get_resource")
async def test_generate_logo_url(get_resource_mock):
    resource_mock = MagicMock()
    resource_mock.meta.client.generate_presigned_url.return_value = (
        "https://www.image_link_here.com"
    )
    get_resource_mock.return_value = resource_mock
    result = await BankVisualIdentityRepository.generate_logo_url("/file_path")
    assert resource_mock.meta.client.generate_presigned_url.called
    assert type(result) == str
