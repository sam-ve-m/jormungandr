from abc import ABC, abstractmethod
from typing import List, Any


class IStateEnumRepository(ABC):
    @abstractmethod
    def get_state_enum(self, country: str) -> List[Any]:
        pass

    @abstractmethod
    def _get_state_cached_enum(self, query: str, country: str) -> List[Any]:
        pass
