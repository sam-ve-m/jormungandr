from etria_logger import Gladsheim

from src.core.interfaces.service.document_issuer_enum.interface import (
    IDocumentIssuerEnumService,
)
from src.domain.response.model import ResponseModel
from src.domain.response.status_code.enums import StatusCode
from src.repository.document_issuer_enum.repository import DocumentIssuerEnumRepository


class DocumentIssuerEnumService(IDocumentIssuerEnumService):
    @classmethod
    def get_response(cls):
        service_response = []

        enums = DocumentIssuerEnumRepository.get_document_issuer_enum()
        for code, value in enums:
            service_response.append({"code": code, "value": value})

        service_response = ResponseModel.build_response(
            success=True, code=StatusCode.SUCCESS, message=None, result=service_response
        )
        return service_response
