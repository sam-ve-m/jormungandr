from abc import ABC, abstractmethod
from typing import List, Any


class IExperienceTimeEnumRepository(ABC):
    @abstractmethod
    def get_experience_time_enum(self) -> List[Any]:
        pass

    @abstractmethod
    def _get_experience_time_cached_enum(self, query: str) -> List[Any]:
        pass
