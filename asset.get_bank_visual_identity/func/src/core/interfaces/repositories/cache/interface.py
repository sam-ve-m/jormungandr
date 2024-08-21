from abc import ABC, abstractmethod
from typing import Any


class ICacheRepository(ABC):
    @abstractmethod
    def save_logo_in_cache(self, logo_link: str, bank_code: str, time: int):
        pass

    @abstractmethod
    def get_cached_logo(self, bank_code: str) -> Any:
        pass
