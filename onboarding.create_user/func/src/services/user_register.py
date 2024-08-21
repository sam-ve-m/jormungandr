from ..domain.exceptions.exceptions import EmailAlreadyExists
from ..domain.models.device_info import DeviceInfo
from ..domain.user.model import UserModel
from ..domain.validators.validator import UserParams
from ..repositories.user.repository import UserRepository
from ..transports.audit.transport import Audit
from ..transports.iara.transport import IaraClient


class UserService:
    def __init__(self, payload_validated: UserParams, device_info: DeviceInfo):
        self.email = payload_validated.email
        self.nick_name = payload_validated.nick_name
        self.device_info = device_info

    async def register(self) -> bool:
        user_model = UserModel(
            email=self.email, nick_name=self.nick_name, device_info=self.device_info
        )
        user_template = await user_model.get_user_template()
        await Audit.record_message_log(user_model=user_model)
        await UserRepository.insert_one_user(user_template=user_template)
        await IaraClient.send_to_email_verification_queue(user_model=user_model)
        return True

    async def verify_email_already_exists(self):
        email_in_use = await UserRepository.find_one_by_email(email=self.email)
        if email_in_use:
            raise EmailAlreadyExists
