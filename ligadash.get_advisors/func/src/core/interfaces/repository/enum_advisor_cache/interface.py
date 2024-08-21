from abc import ABC, abstractmethod
from typing import Any


class IEnumAdvisorCacheRepository(ABC):
    @abstractmethod
    def save_enum_advisor(self, enum_advisor: Any, time: int):
        pass

    @abstractmethod
    def get_enum_advisor(self) -> Any:
        pass
