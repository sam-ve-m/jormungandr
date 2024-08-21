from abc import ABC, abstractmethod


class IDocumentTypeEnumService(ABC):
    @abstractmethod
    def get_response(self):
        pass
