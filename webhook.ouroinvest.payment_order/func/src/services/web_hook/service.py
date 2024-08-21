# PROJECT IMPORTS
from src.domain.validator.webhook.validator import WebHookMessage
from src.transport.bifrost.transport import BifrostTransport
from src.repositories.payment_order.repository import PaymentOrderRepository


class ForexAccountService:

    @classmethod
    async def request_payment_order_process(cls, webhook_message: WebHookMessage) -> bool:
        await PaymentOrderRepository.save_payment_order(webhook_message=webhook_message)
        result = await BifrostTransport.send_payment_order_to_process(
            webhook_message=webhook_message
        )
        return result
