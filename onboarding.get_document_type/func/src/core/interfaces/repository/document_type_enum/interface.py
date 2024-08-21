from abc import ABC, abstractmethod
from typing import List, Any


class IDocumentTypeEnumRepository(ABC):
    @abstractmethod
    def get_document_type_enum(self) -> List[Any]:
        pass

    @abstractmethod
    def _get_document_type_cached_enum(self, query: str) -> List[Any]:
        pass
