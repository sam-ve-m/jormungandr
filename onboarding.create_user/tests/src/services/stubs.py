import asyncio

from func.src.domain.models.device_info import DeviceInfo
from func.src.domain.user.model import UserModel
from func.src.domain.validators.validator import UserParams

stub_payload_validated = UserParams(
    **{
        "email": "teste@teste.com",
        "nick_name": "vnnstar",
    }
)

stub_device_info = DeviceInfo({"precision": 1}, "")

stub_user_model = UserModel(
    email=stub_payload_validated.email,
    nick_name=stub_payload_validated.nick_name,
    device_info=stub_device_info,
)


stub_user_model_template = asyncio.run(stub_user_model.get_user_template())
