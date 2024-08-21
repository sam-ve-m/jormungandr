from abc import ABC, abstractmethod
from typing import List, Any


class IDocumentIssuerEnumRepository(ABC):
    @abstractmethod
    def get_document_issuer_enum(self) -> List[Any]:
        pass

    @abstractmethod
    def _get_document_issuer_cached_enum(self, query: str) -> List[Any]:
        pass
