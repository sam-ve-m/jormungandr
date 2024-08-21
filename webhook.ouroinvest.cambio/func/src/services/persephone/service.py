# THIRD PARTY IMPORTS
from decouple import config
from etria_logger import Gladsheim
from persephone_client import Persephone

# PROJECT IMPORTS
from func.src.domain.enums.persephone_queue.enum import PersephoneQueue
from func.src.domain.models.persephone.model import LogOuroInvestToPersephone


class SendToPersephone:

    @classmethod
    async def register_exchange_ouroinvest_member_log(
            cls,
            unique_id: str,
            status: str,
            cpf: str,
            exchange_account: dict
    ):

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await Persephone.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC"),
            partition=PersephoneQueue.OUROINVEST_EXCHANGE.value,
            message=LogOuroInvestToPersephone.exchange_ouroinvest_schema_message(
                unique_id=unique_id,
                status=status,
                cpf=cpf,
                exchange_account=exchange_account
            ),
            schema_name=config("PERSEPHONE_SCHEMA"),
        )
        if sent_to_persephone is False:
            Gladsheim.error(
                message="SendToPersephone::register_exchange_ouroinvest_member_log::Error on trying to register log")
            raise NotSentToPersephone
