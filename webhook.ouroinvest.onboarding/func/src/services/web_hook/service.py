# PROJECT IMPORTS
from src.domain.enums.ouroinvest_status.enum import OuroInvestStatus
from src.domain.exceptions.exceptions import UserWasNotFound, UserWasNotUpdated
from src.domain.validator.webhook.validator import WebHookMessage
from src.repositories.user.repository import UserRepository
from src.transport.iara.transport import IaraTransport
from src.transport.persephone.transport import SendToPersephone


class ExchangeAccountService:
    @classmethod
    async def save_exchange_account(cls, webhook_message: WebHookMessage) -> bool:
        unique_id = await UserRepository.find_client_unique_id(webhook_message.cpf)
        if not unique_id:
            raise UserWasNotFound

        await SendToPersephone.register_user_exchange_member_log(
            webhook_message=webhook_message,
            unique_id=unique_id
        )

        was_updated = await UserRepository.update_exchange_account_status(webhook_message)
        if was_updated is False:
            raise UserWasNotUpdated()

        if webhook_message.status == OuroInvestStatus.CONCLUIDO:
            await IaraTransport.save_account_exchange(unique_id)

        return was_updated
