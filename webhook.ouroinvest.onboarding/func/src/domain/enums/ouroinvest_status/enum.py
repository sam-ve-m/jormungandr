# STANDARD IMPORTS
from enum import Enum


class OuroInvestStatus(Enum):
    EM_ANALISE = 'Em Análise'
    CONCLUIDO = 'Concluído'
    EM_PROCESSAMENTO = 'Em Processamento'

    def __repr__(self):
        return self.value
