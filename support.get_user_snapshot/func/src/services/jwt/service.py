# Jormungandr
from ...domain.exceptions import InvalidJwtToken

# Third party
from heimdall_client import Heimdall, HeimdallStatusResponses


class JwtService:
    @classmethod
    async def get_valid_jwt_content(cls, jwt: str) -> dict:
        is_valid_jwt = await Heimdall.validate_jwt(jwt=jwt)
        if not is_valid_jwt:
            raise InvalidJwtToken("Invalid token")
        jwt_content, heimdall_status_response = await Heimdall.decode_payload(jwt=jwt)
        if heimdall_status_response != HeimdallStatusResponses.SUCCESS:
            raise InvalidJwtToken("Fail to decode jwt")
        content = jwt_content["decoded_jwt"]
        return content
