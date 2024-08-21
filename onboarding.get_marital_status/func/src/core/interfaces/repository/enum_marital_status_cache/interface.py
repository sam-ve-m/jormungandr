from abc import ABC, abstractmethod
from typing import Any


class IEnumMaritalStatusCacheRepository(ABC):
    @abstractmethod
    def save_enum_marital_status(self, enum_marital_status: Any, time: int):
        pass

    @abstractmethod
    def get_enum_marital_status(self) -> Any:
        pass
