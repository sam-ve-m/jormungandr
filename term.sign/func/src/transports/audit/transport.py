from decouple import config
from etria_logger import Gladsheim
from persephone_client import Persephone

from ...domain.enums.types import QueueTypes
from ...domain.exceptions.exceptions import ErrorOnSendAuditLog
from ...domain.terms.model import TermsModel


class Audit:
    audit_client = Persephone

    @classmethod
    async def record_message_log(cls, terms_model: TermsModel) -> bool:
        message = terms_model.get_user_terms_signed_audit_template()
        partition = QueueTypes.TERM_QUEUE
        topic = config("PERSEPHONE_TOPIC_USER")
        schema_name = config("PERSEPHONE_USER_TERMS_SIGN_SCHEMA")
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
                message="Audit::register_user_log::Error on trying to register log"
            )
            raise ErrorOnSendAuditLog()
        return True
