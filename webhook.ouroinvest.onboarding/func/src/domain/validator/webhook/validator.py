import re

import orjson
from pydantic import BaseModel, validator

from src.domain.enums.ouroinvest_status.enum import OuroInvestStatus
from src.domain.exceptions.exceptions import StatusSentIsNotValid


class WebHookMessage(BaseModel):
    status: OuroInvestStatus
    cpf: str

    @validator("cpf")
    def unmask_cpf(cls, cpf_raw: str):
        cpf = re.sub("[^0-9]", "", cpf_raw)
        return cpf

    @classmethod
    def from_request(cls, request_body: dict):
        message = orjson.loads(request_body.get("mensagem"))
        status = message.get("statusCadastro")
        cpf = message.get("inscricao")
        return cls(status=status, cpf=cpf)

    def log_schema(self, unique_id: str) -> dict:
        schema = {
            "status": self.status,
            "unique_id": unique_id,
        }
        return schema
