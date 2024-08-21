from abc import ABC, abstractmethod
from typing import Any


class IEnumDocumentTypeCacheRepository(ABC):
    @abstractmethod
    def save_enum_document_type(self, enum_document_type: Any, time: int):
        pass

    @abstractmethod
    def get_enum_document_type(self) -> Any:
        pass
