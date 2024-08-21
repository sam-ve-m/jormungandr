from abc import ABC, abstractmethod
from typing import Any


class IEnumStateCacheRepository(ABC):
    @abstractmethod
    def save_enum_state(self, enum_state: Any, country: str, time: int):
        pass

    @abstractmethod
    def get_enum_state(self, country: str) -> Any:
        pass
