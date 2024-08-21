from abc import ABC, abstractmethod
from typing import List, Any


class IGenderEnumRepository(ABC):
    @abstractmethod
    def get_gender_enum(self) -> List[Any]:
        pass

    @abstractmethod
    def _get_gender_cached_enum(self, query: str) -> List[Any]:
        pass
