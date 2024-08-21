# Jormungandr
from ...domain.exceptions.service.exception import ErrorOnDecodeJwt

# Third party
from heimdall_client import Heimdall
from heimdall_client.src.domain.enums.heimdall_status_responses import (
    HeimdallStatusResponses,
)


class JwtService:
    @staticmethod
    async def validate_jwt(jwt: str) -> bool:
        jwt_content, heimdall_status_response = await Heimdall.decode_payload(jwt=jwt)
        if not HeimdallStatusResponses.SUCCESS.value == heimdall_status_response.value:
            raise ErrorOnDecodeJwt()
        return True
