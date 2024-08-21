class LogOuroInvestToPersephone:

    @classmethod
    def exchange_ouroinvest_schema_message(
            cls,
            exchange_data: dict,
            cpf: str,
            status: str,
            unique_id: str
    ) -> dict:
        message = {
            "unique_id": unique_id,
            "status": status,
            "cpf": cpf,
            "exchange_data": exchange_data
        }

        return message
