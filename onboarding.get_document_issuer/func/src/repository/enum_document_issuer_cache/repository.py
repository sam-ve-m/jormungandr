from typing import Union

from etria_logger import Gladsheim
from mnemosine import SyncCache

from src.core.interfaces.repository.enum_document_issuer_cache.interface import (
    IEnumDocumentIssuerCacheRepository,
)


class EnumDocumentIssuerCacheRepository(IEnumDocumentIssuerCacheRepository):
    enum_key = "jormungandr:EnumDocumentIssuer"

    @classmethod
    def save_enum_document_issuer(
        cls, enum_document_issuer: list, time: int = 3600
    ) -> bool:
        try:
            SyncCache.save(cls.enum_key, list(enum_document_issuer), int(time))
            return True
        except ValueError as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            return False
        except TypeError as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            return False
        except Exception as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            return False

    @classmethod
    def get_enum_document_issuer(cls) -> Union[list, None]:
        result = SyncCache.get(cls.enum_key)
        return result
