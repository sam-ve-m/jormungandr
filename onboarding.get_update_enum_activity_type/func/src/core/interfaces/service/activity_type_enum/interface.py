from abc import ABC, abstractmethod


class IActivityTypeEnumService(ABC):
    @abstractmethod
    def get_response(self):
        pass
