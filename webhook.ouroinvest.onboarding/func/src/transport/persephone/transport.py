# THIRD PARTY IMPORTS
from decouple import config
from etria_logger import Gladsheim
from persephone_client import Persephone

# PROJECT IMPORTS
from src.domain.exceptions.exceptions import NotSentToPersephone
from src.domain.validator.webhook.validator import WebHookMessage


class SendToPersephone:

    @classmethod
    async def register_user_exchange_member_log(
            cls, unique_id: str,
            webhook_message: WebHookMessage
    ):
        message = webhook_message.log_schema(unique_id)
        success, sent_status = await Persephone.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC"),
            partition=int(config("PERSEPHONE_PARTITION")),
            message=message,
            schema_name=config("PERSEPHONE_SCHEMA"),
        )
        if success is False:
            Gladsheim.error(
                message="SendToPersephone::register_user_exchange_member_log::Error on trying to register log",
                status=sent_status,
            )
            raise NotSentToPersephone()
