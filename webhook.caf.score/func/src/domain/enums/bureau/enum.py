from enum import Enum


class BureauType(Enum):
    process_started = 'process_started'
    status_updated = 'status_updated'
    documentscopy_requested = 'documentscopy_requested'

    def __repr__(self):
        return self.value


class BureauStatus(Enum):
    PROCESSING = "PROCESSANDO"
    APPROVED = "APROVADO"
    REPROVED = "REPROVADO"
    PENDING = "PENDENTE"

    def __repr__(self):
        return self.value


# PROCESSANDO: o documento está sendo processado e pode ter seus dados alterados.
# APROVADO: o documento foi aprovado em todas as regras configuradas no relatório.
# PENDENTE: o documento tem alguma irregularidade. Você pode aprovar ou reprovar este documento no seu back-office (conforme suas regras).
# PENDENTE OCR não foi possível identificar o documento nas imagens enviadas nem realizar OCR. Neste cenário pode-se optar por informar os dados manualmente ou reprovar o documento no seu back-office (conforme suas regras).
# REPROVADO: recomendamos reprovar este documento, pois há indicios de fraude ou alguma irregularidade (saiba mais em: reprovado x suspeita fraude).
