from abc import ABC, abstractmethod


class IExperienceTimeEnumService(ABC):
    @abstractmethod
    def get_response(self):
        pass
