from abc import ABC, abstractmethod


class IBrokerageTypeEnumService(ABC):
    @abstractmethod
    def get_response(self):
        pass
