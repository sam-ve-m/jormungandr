from abc import ABC, abstractmethod
from typing import List, Any


class ICountryEnumRepository(ABC):
    @abstractmethod
    def get_country_enum(self) -> List[Any]:
        pass

    @abstractmethod
    def _get_country_cached_enum(self, query: str) -> List[Any]:
        pass
