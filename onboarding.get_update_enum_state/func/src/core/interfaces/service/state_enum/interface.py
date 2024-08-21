from abc import ABC, abstractmethod

from func.src.domain.validators.state.validator import StateParams


class IStateEnumService(ABC):
    @abstractmethod
    def get_response(self, request: StateParams):
        pass
