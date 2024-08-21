# Jormungandr-Onboarding
from ...domain.enums.types import QueueTypes
from ...domain.exceptions.transports.exception import ErrorOnSendAuditLog
from ...domain.suitability.model import SuitabilityModel

# Third party
from decouple import config
from etria_logger import Gladsheim
from persephone_client import Persephone


class Audit:
    audit_client = Persephone

    @classmethod
    async def record_message_log(cls, suitability_model: SuitabilityModel) -> bool:
        message = await suitability_model.get_audit_suitability_template()
        partition = QueueTypes.SUITABILITY
        topic = config("PERSEPHONE_TOPIC_USER")
        schema_name = config("PERSEPHONE_SUITABILITY_SCHEMA")
        (
            success,
            status_sent_to_persephone,
        ) = await cls.audit_client.send_to_persephone(
            topic=topic,
            partition=partition,
            message=message,
            schema_name=schema_name,
        )
        if not success:
            Gladsheim.error(
                message="Audit::record_message_log::Error when trying to register suitability log"
            )
            raise ErrorOnSendAuditLog()
        return True
