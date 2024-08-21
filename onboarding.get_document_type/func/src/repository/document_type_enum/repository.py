from typing import List, Tuple

from func.src.core.interfaces.repository.document_type_enum.interface import IDocumentTypeEnumRepository
from func.src.repository.enum_document_type_cache.repository import EnumDocumentTypeCacheRepository
from func.src.repository.base_repository.oracle.repository import OracleBaseRepository


class DocumentTypeEnumRepository(IDocumentTypeEnumRepository):

    enum_query = "SELECT CODE as code, DESCRIPTION as description FROM USPIXDB001.SINCAD_EXTERNAL_IDENTIFICATION_TYPE"

    @classmethod
    def get_document_type_enum(cls) -> List[Tuple]:
        sql = cls.enum_query
        result = cls._get_document_type_cached_enum(sql)
        return result

    @classmethod
    def _get_document_type_cached_enum(cls, query: str) -> List[Tuple]:
        if cached_enum := EnumDocumentTypeCacheRepository.get_enum_document_type():
            return cached_enum

        enum_values = OracleBaseRepository.query(sql=query)
        EnumDocumentTypeCacheRepository.save_enum_document_type(enum_values)
        return enum_values
