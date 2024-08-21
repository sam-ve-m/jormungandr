from abc import ABC, abstractmethod


class ICountryEnumService(ABC):
    @abstractmethod
    def get_response(self):
        pass
