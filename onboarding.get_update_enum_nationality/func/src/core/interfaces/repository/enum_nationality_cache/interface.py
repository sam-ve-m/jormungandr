from abc import ABC, abstractmethod
from typing import Any


class IEnumNationalityCacheRepository(ABC):
    @abstractmethod
    def save_enum_nationality(self, enum_nationality: Any, time: int):
        pass

    @abstractmethod
    def get_enum_nationality(self) -> Any:
        pass
