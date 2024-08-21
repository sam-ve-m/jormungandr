from typing import Optional

from decouple import config

from src.core.interfaces.repositories.terms.interface import (
    ITermRepository,
)
from src.domain.enums.terms.enum import TermsFileType
from src.domain.exceptions.exceptions import FileNotFound
from src.infrastructures.s3.s3 import S3Infrastructure


class TermRepository(ITermRepository):
    link_expiration_time = config("LINK_EXPIRATION_TIME_IN_SECONDS")
    bucket_name = config("AWS_BUCKET_NAME")

    @classmethod
    async def _get_last_saved_file_from_folder(
        cls, folder_path: str, bucket_name: str
    ) -> Optional[str]:
        objects = list()
        async with S3Infrastructure.get_resource() as s3_resource:
            bucket = await s3_resource.Bucket(bucket_name)
            async for s3_object in bucket.objects.filter(
                Prefix=folder_path, Delimiter="/"
            ):
                objects.append(s3_object)

        objects = sorted(objects, key=lambda item: item.meta.data.get("LastModified"), reverse=True)

        if len(objects) == 0:
            raise FileNotFound(
                f"File not found in S3. Path: {folder_path}, Bucket: {bucket_name}"
            )

        latest_file = objects[0]
        file_key = latest_file.key
        return file_key

    @staticmethod
    def _resolve_term_path(term: TermsFileType) -> str:
        return f"{term.value}/"

    @classmethod
    async def _generate_term_url(cls, term_path: str) -> str:
        async with S3Infrastructure.get_client() as s3_client:
            logo_url = await s3_client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": cls.bucket_name, "Key": term_path},
                ExpiresIn=cls.link_expiration_time,
            )
        return logo_url

    @classmethod
    async def get_term_link(cls, term: TermsFileType) -> str:
        term_path = cls._resolve_term_path(term)
        file = await cls._get_last_saved_file_from_folder(term_path, cls.bucket_name)
        link = await cls._generate_term_url(file)
        return link
