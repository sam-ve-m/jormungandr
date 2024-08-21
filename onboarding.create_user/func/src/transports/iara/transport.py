# Jormungandr
from ...domain.exceptions.exceptions import ErrorOnSendIaraMessage
from ...domain.user.model import UserModel

# Third party
from etria_logger import Gladsheim
from iara_client import Iara, IaraTopics, SchemaTypes


class IaraClient:
    @staticmethod
    async def send_to_email_verification_queue(user_model: UserModel):
        message = await user_model.get_iara_user_template()
        topic = IaraTopics.EMAIL_VALIDATION
        schema_type = SchemaTypes.EMAIL_VALIDATION

        success, status_sent_to_iara = await Iara.send_to_iara(
            message=message,
            schema_type=schema_type,
            topic=topic,
        )
        if not success:
            Gladsheim.error(
                message=f"Iara_client::send_to_email_verification_queue::Error when trying to send to"
                f" iara::{message=}::{schema_type=}::{topic=}"
            )
            raise ErrorOnSendIaraMessage
        return True
