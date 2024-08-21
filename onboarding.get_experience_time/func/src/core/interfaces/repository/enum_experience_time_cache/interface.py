from abc import ABC, abstractmethod
from typing import Any


class IEnumExperienceTimeCacheRepository(ABC):
    @abstractmethod
    def save_enum_experience_time(self, enum_experience_time: Any, time: int):
        pass

    @abstractmethod
    def get_enum_experience_time(self) -> Any:
        pass
