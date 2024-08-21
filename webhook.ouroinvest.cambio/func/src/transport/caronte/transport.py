from decouple import config


class CaronteTransport:

    @classmethod
    async def get_transaction_snapshot(cls, client_code: int, transaction_code: int) -> dict:
        url = config("OUROINVEST_GET_TRANSACTION_SNAPSHOT_URL").format(transaction_code, client_code)
        response = await cls.ouroinvest_transport.request(HTTPMethods.GET, url, client_code)
        snapshot = await response.json()
        return snapshot
