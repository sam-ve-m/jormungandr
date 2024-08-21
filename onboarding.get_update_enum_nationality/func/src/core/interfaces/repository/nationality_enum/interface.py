from abc import ABC, abstractmethod
from typing import List, Any


class INationalityEnumRepository(ABC):
    @abstractmethod
    def get_nationality_enum(self) -> List[Any]:
        pass

    @abstractmethod
    def _get_nationality_cached_enum(self, query: str) -> List[Any]:
        pass
