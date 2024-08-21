import orjson
from dataclasses import dataclass

from func.src.domain.enums.bureau.enum import BureauType, BureauStatus
from func.src.domain.exceptions.exceptions import InvalidMessageTypeReceived, InvalidStatusReceived


@dataclass
class WebHookMessage:
    event_type: BureauType
    status: BureauStatus
    status_reasons: list
    template_id: str
    report: str
    uuid: str
    date: str

    @classmethod
    def from_request(cls, request_body: dict):
        status_reasons = request_body.get("statusReasons")
        event_type = request_body.get("type")
        status = request_body.get("status")
        if event_type not in BureauType.__dict__:
            raise InvalidMessageTypeReceived(event_type)
        elif status not in BureauStatus.__dict__:
            raise InvalidStatusReceived(status)
        template_id = request_body.get("templateId")
        report = request_body.get("report")
        uuid = request_body.get("uuid")
        date = request_body.get("date")
        return cls(
            date=date,
            uuid=uuid,
            report=report,
            template_id=template_id,
            status=BureauStatus[status],
            status_reasons=status_reasons,
            event_type=BureauType[event_type],
        )

    def log_schema(self, cpf: str) -> dict:
        schema = {
            "cpf": cpf,
            "status": self.status.value,
        }
        return schema
