from typing import Optional

from decouple import config

from func.src.core.interfaces.repositories.terms.interface import (
    ITermRepository,
)
from func.src.domain.enums.terms import TermsFileType
from func.src.infrastructures.s3.s3 import S3Infrastructure


class TermRepository(ITermRepository):
    __link_expiration_time = config("LINK_EXPIRATION_TIME_IN_SECONDS")
    __bucket_name = config("AWS_BUCKET_NAME")
    __file_extension_by_type = {
        TermsFileType.TERM_APPLICATION: ".pdf",
        TermsFileType.TERM_OPEN_ACCOUNT: ".pdf",
        TermsFileType.TERM_REFUSAL: ".pdf",
        TermsFileType.TERM_NON_COMPLIANCE: ".pdf",
        TermsFileType.TERM_RETAIL_LIQUID_PROVIDER: ".pdf",
        TermsFileType.TERM_AND_PRIVACY_POLICY_DATA_SHARING_POLICY_DL_PT: ".pdf",
        TermsFileType.TERM_AND_PRIVACY_POLICY_DATA_SHARING_POLICY_DL_US: ".pdf",
        TermsFileType.TERM_OPEN_ACCOUNT_DL_PT: ".pdf",
        TermsFileType.TERM_OPEN_ACCOUNT_DL_US: ".pdf",
        TermsFileType.TERM_BUSINESS_CONTINUITY_PLAN_DL_PT: ".pdf",
        TermsFileType.TERM_BUSINESS_CONTINUITY_PLAN_DL_US: ".pdf",
        TermsFileType.TERM_CUSTOMER_RELATIONSHIP_SUMMARY_DL_PT: ".pdf",
        TermsFileType.TERM_CUSTOMER_RELATIONSHIP_SUMMARY_DL_US: ".pdf",
        TermsFileType.TERM_OUROINVEST: ".pdf",
        TermsFileType.TERM_GRINGO_WORLD: ".pdf",
        TermsFileType.TERM_GRINGO_WORLD_GENERAL_ADVICES: ".pdf",
        TermsFileType.TERM_MISMATCH_PROFILE: ".pdf",
    }

    @staticmethod
    def __resolve_term_path(term: TermsFileType) -> str:
        return f"{term.value}/"

    @staticmethod
    def __generate_term_file_name(name: str, version: str):
        return f"{name}_v{version}"

    @classmethod
    def __get_file_extension_by_type(cls, file_type: TermsFileType) -> Optional[str]:
        return cls.__file_extension_by_type.get(file_type)

    @classmethod
    async def _generate_term_url(
        cls, term_path: str, file_name: str, file_extension: str
    ) -> str:
        async with S3Infrastructure.get_client() as s3_client:
            logo_url = await s3_client.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": cls.__bucket_name,
                    "Key": f"{term_path}{file_name}{file_extension}",
                },
                ExpiresIn=cls.__link_expiration_time,
            )
        return logo_url

    @classmethod
    async def get_term_link_by_version(cls, term: TermsFileType, version: str) -> str:
        file_name = cls.__generate_term_file_name(name=term.value, version=version)
        path = cls.__resolve_term_path(term)
        file_extension = cls.__get_file_extension_by_type(term)
        term_link = await cls._generate_term_url(
            term_path=path, file_name=file_name, file_extension=file_extension
        )
        return term_link
