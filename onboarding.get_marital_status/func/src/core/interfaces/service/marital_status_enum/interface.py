from abc import ABC, abstractmethod


class IMaritalStatusEnumService(ABC):
    @abstractmethod
    def get_response(self):
        pass
