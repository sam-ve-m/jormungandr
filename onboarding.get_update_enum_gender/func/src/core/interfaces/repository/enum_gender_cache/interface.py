from abc import ABC, abstractmethod
from typing import Any


class IEnumGenderCacheRepository(ABC):
    @abstractmethod
    def save_enum_gender(self, enum_gender: Any, time: int):
        pass

    @abstractmethod
    def get_enum_gender(self) -> Any:
        pass
