from abc import ABC, abstractmethod
from typing import List, Any


class IMaritalStatusEnumRepository(ABC):
    @abstractmethod
    def get_marital_status_enum(self) -> List[Any]:
        pass

    @abstractmethod
    def _get_marital_status_cached_enum(self, query: str) -> List[Any]:
        pass
