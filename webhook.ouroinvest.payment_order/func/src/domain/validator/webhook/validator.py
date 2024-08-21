import re
from datetime import datetime

import orjson
from pydantic import BaseModel


class WebHookMessage(BaseModel):
    client_id: int
    account_id: int
    payment_order_id: int
    currency_id: int
    currency_name: str
    value: float
    register_date: datetime
    income_date: datetime
    origin: str

    @classmethod
    def from_request(cls, request_body: dict):
        message = orjson.loads(request_body.get("mensagem"))

        client_id = message.get("CodigoCliente")
        account_id = message.get("CodigoConta")
        payment_order_id = message.get("CodigoOrdemPagamento")
        currency_id = message.get("CdMoeda")
        currency_name = message.get("SimboloMoeda")
        value = message.get("ValorMonetario")
        register_date = message.get("DataCadastroOrdem")
        income_date = message.get("DataRecebimento")
        origin = message.get("Ordenante")

        return cls(
            client_id=client_id,
            account_id=account_id,
            payment_order_id=payment_order_id,
            currency_id=currency_id,
            currency_name=currency_name,
            value=value,
            register_date=register_date,
            income_date=income_date,
            origin=origin,
        )
