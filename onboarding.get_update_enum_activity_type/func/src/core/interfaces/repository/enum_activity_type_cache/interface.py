from abc import ABC, abstractmethod
from typing import Any


class IEnumActivityTypeCacheRepository(ABC):
    @abstractmethod
    def save_enum_activity_type(self, enum_activity_type: Any, time: int):
        pass

    @abstractmethod
    def get_enum_activity_type(self) -> Any:
        pass
