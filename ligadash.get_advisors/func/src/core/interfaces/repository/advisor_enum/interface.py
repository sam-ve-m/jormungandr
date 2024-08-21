from abc import ABC, abstractmethod
from typing import List, Any


class IAdvisorEnumRepository(ABC):
    @abstractmethod
    def get_advisor_enum(self) -> List[Any]:
        pass

    @abstractmethod
    def _get_advisor_cached_enum(self, query: str) -> List[Any]:
        pass
