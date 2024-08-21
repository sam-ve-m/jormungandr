from decouple import config
from persephone_client import Persephone

from ...domain.enums.queue.types import QueueTypes
from ...domain.exceptions.exceptions import ErrorOnSendAuditLog
from ...domain.user.model import UserModel


class Audit:
    audit_client = Persephone

    @classmethod
    async def record_message_log(cls, user_model: UserModel):
        message = await user_model.get_audit_prospect_user_template()
        partition = QueueTypes.PROSPECT_USER
        topic = config("PERSEPHONE_TOPIC_USER")
        schema_name = config("PERSEPHONE_CREATE_USER_SCHEMA")
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
            raise ErrorOnSendAuditLog
        return True
