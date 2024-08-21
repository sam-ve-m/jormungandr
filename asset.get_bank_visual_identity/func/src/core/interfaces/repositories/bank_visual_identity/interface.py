from abc import ABC, abstractmethod


class IBankVisualIdentityRepository(ABC):
    @classmethod
    @abstractmethod
    async def logo_exists(cls, logo_path: str) -> bool:
        pass

    @classmethod
    @abstractmethod
    async def generate_logo_url(cls, logo_path: str) -> str:
        pass
