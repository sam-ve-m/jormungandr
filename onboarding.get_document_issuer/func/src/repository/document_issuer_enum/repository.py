from typing import List, Tuple

from src.core.interfaces.repository.document_issuer_enum.interface import (
    IDocumentIssuerEnumRepository,
)
from src.repository.enum_document_issuer_cache.repository import (
    EnumDocumentIssuerCacheRepository,
)
from src.repository.base_repository.oracle.repository import OracleBaseRepository


class DocumentIssuerEnumRepository(IDocumentIssuerEnumRepository):

    enum_query = "SELECT CODE as code, DESCRIPTION as description FROM USPIXDB001.SINCAD_EXTERNAL_ISSUER"

    @classmethod
    def get_document_issuer_enum(cls) -> List[Tuple]:
        sql = cls.enum_query
        result = cls._get_document_issuer_cached_enum(sql)
        return result

    @classmethod
    def _get_document_issuer_cached_enum(cls, query: str) -> List[Tuple]:
        if cached_enum := EnumDocumentIssuerCacheRepository.get_enum_document_issuer():
            return cached_enum

        enum_values = OracleBaseRepository.query(sql=query)
        EnumDocumentIssuerCacheRepository.save_enum_document_issuer(enum_values)
        return enum_values
