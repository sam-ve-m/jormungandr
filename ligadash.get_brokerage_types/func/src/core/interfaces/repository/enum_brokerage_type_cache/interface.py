from abc import ABC, abstractmethod
from typing import Any


class IEnumBrokerageTypeCacheRepository(ABC):
    @abstractmethod
    def save_enum_brokerage_type(self, enum_brokerage_type: Any, time: int):
        pass

    @abstractmethod
    def get_enum_brokerage_type(self) -> Any:
        pass
