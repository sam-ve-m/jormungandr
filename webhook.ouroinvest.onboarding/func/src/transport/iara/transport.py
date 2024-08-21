from iara_client import Iara, IaraTopics

from src.domain.exceptions.exceptions import NotSentToIara


class IaraTransport:
    @staticmethod
    async def save_account_exchange(unique_id: str):
        success, reason = await Iara.send_to_iara(
            topic=IaraTopics.OURO_INVESTE_BASIC_REGISTRATION_DETAILS,
            message={"unique_id": unique_id},
        )
        if not success:
            raise NotSentToIara(str(reason))
