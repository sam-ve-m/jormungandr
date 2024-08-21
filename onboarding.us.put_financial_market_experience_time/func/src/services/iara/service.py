from etria_logger import Gladsheim
from iara_client import Iara, IaraTopics, SchemaTypes

from func.src.domain.models.iara_message.model import IaraMessage
from func.src.domain.models.jwt.models import Jwt
from func.src.domain.exceptions.exceptions import ErrorLoggingOnIara


class SendToIara:
    @classmethod
    async def send_user_to_dw_registration(cls, jwt_data: Jwt):

        (is_message_sent, iara_client_status,) = await Iara.send_to_iara(
            topic=IaraTopics.DW_REGISTRATION,
            message=IaraMessage.user_time_experience_iara_schema(
                unique_id=jwt_data.get_unique_id_from_jwt_payload()
            ),
            schema_type=SchemaTypes.DW_REGISTRATION,
        )

        if is_message_sent is False:
            Gladsheim.error(
                message="SendToIara::send_user_to_dw_registration::Error on trying to register log"
            )
            raise ErrorLoggingOnIara()
