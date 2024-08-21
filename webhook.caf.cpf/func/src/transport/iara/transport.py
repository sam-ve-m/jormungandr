from iara_client import Iara, IaraTopics

from func.src.domain.exceptions.exceptions import ErrorSendingToIaraDatailCpfValidation


class BureauApiTransport:
    @staticmethod
    async def detail_transaction(cpf: str):
        success, reason = await Iara.send_to_iara(
            topic=IaraTopics.CAF_CPF_VALIDATION_DETAILS,
            message={"cpf": cpf},
        )
        if not success:
            raise ErrorSendingToIaraDatailCpfValidation(str(reason))
        return True
