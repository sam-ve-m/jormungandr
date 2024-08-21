# Jormungandr - Onboarding
from ...infrastructures.s3.infrastructure import S3Infrastructure
from ...domain.enums.types import TermsType

# Third party
from etria_logger import Gladsheim
from decouple import config


class FileRepository:
    infra = S3Infrastructure

    @classmethod
    async def get_current_term_version(cls, term_type: TermsType) -> int:
        version, path = 0, cls._resolve_term_path(term_type)
        try:
            async with cls.infra.get_resource() as s3_resource:
                bucket = await s3_resource.Bucket(config("AWS_BUCKET_TERMS"))
                async for s3_object in bucket.objects.filter(
                    Prefix=path, Delimiter="/"
                ):
                    version += 1
            return version
        except Exception as ex:
            Gladsheim.error(error=ex)
            raise ex

    @staticmethod
    def _resolve_term_path(term: TermsType) -> str:
        return f"{term.value}/"
