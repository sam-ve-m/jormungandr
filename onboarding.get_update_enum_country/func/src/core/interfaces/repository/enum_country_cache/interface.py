from abc import ABC, abstractmethod
from typing import Any


class IEnumCountryCacheRepository(ABC):
    @abstractmethod
    def save_enum_country(self, enum_country: Any, time: int):
        pass

    @abstractmethod
    def get_enum_country(self) -> Any:
        pass
