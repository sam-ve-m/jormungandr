from abc import ABC, abstractmethod


class INationalityEnumService(ABC):
    @abstractmethod
    def get_response(self):
        pass
