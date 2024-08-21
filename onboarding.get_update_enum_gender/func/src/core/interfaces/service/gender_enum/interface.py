from abc import ABC, abstractmethod


class IGenderEnumService(ABC):
    @abstractmethod
    def get_response(self):
        pass
