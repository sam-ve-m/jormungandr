from abc import ABC, abstractmethod
from typing import List, Any


class IBrokerageTypeEnumRepository(ABC):
    @abstractmethod
    def get_brokerage_type_enum(self) -> List[Any]:
        pass

    @abstractmethod
    def _get_brokerage_type_cached_enum(self, query: str) -> List[Any]:
        pass
