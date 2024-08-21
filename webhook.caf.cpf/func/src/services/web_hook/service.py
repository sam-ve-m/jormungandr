import asyncio

from func.src.domain.validator.webhook.validator import WebHookMessage
from func.src.repositories.bureau_transactions.repository import BureauTransactionRepository
from func.src.repositories.user.repository import UserRepository
from func.src.transport.iara.transport import BureauApiTransport
from func.src.transport.persephone.transport import SendToPersephone


class BureauValidationService:
    @classmethod
    async def save_bureau_validation(cls, webhook_message: WebHookMessage) -> bool:
        cpf = await BureauTransactionRepository.get_user_cpf_of_transaction(webhook_message)
        await SendToPersephone.register_user_cpf_validation_log(cpf, webhook_message)
        update_transaction = BureauTransactionRepository.update_bureau_transaction(webhook_message)
        send_to_iara = BureauApiTransport.detail_transaction(cpf)
        update_user = UserRepository.update_bureau_validation(cpf, webhook_message)
        success = all(await asyncio.gather(
            update_user, update_transaction, send_to_iara
        ))
        return success
