# Jormungandr
from ...domain.exceptions.transports.exception import SignTermStatusCodeNotOk

# Standards
from http import HTTPStatus

# Third party
from decouple import config
from etria_logger import Gladsheim
from httpx import AsyncClient


class TermTransport:
    @staticmethod
    async def sign_term(jwt: str, body: dict, device_info: str) -> bool:
        headers = {"x-thebes-answer": jwt, "x-device-info": device_info}
        async with AsyncClient() as httpx_client:
            request_result = await httpx_client.put(
                config("JORMUNGANDR_SIGN_TERM_URL"), headers=headers, json=body
            )
            if not request_result.status_code == HTTPStatus.OK:
                response_error = request_result.json()
                Gladsheim.error(error=response_error)
                raise SignTermStatusCodeNotOk()
            return True
