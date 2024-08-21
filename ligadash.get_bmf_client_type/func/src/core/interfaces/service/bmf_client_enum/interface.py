from abc import ABC, abstractmethod


class IBmfClientEnumService(ABC):
    @abstractmethod
    def get_response(self):
        pass
