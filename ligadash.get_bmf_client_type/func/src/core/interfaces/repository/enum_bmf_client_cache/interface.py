from abc import ABC, abstractmethod
from typing import Any


class IEnumBmfClientCacheRepository(ABC):
    @abstractmethod
    def save_enum_bmf_client(self, enum_bmf_client: Any, time: int):
        pass

    @abstractmethod
    def get_enum_bmf_client(self) -> Any:
        pass
