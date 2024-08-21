from abc import ABC, abstractmethod
from typing import List, Any


class IBmfClientEnumRepository(ABC):
    @abstractmethod
    def get_bmf_client_enum(self) -> List[Any]:
        pass

    @abstractmethod
    def _get_bmf_client_cached_enum(self, query: str) -> List[Any]:
        pass
