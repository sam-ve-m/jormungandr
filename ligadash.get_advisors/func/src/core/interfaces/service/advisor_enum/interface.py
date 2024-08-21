from abc import ABC, abstractmethod


class IAdvisorEnumService(ABC):
    @abstractmethod
    def get_response(self):
        pass
