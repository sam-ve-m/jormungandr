from abc import ABC, abstractmethod
from typing import Any


class IEnumDocumentIssuerCacheRepository(ABC):
    @abstractmethod
    def save_enum_document_issuer(self, enum_document_issuer: Any, time: int):
        pass

    @abstractmethod
    def get_enum_document_issuer(self) -> Any:
        pass
