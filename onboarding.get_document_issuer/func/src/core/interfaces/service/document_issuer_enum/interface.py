from abc import ABC, abstractmethod


class IDocumentIssuerEnumService(ABC):
    @abstractmethod
    def get_response(self):
        pass
