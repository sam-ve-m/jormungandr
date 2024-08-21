import asyncio

from func.src.domain.exceptions.exceptions import UniqueIdWasNotUpdate
from func.src.domain.models.device_info.model import DeviceInfo
from func.src.domain.models.jwt.models import Jwt
from func.src.domain.models.time_experience.model import TimeExperienceRequest
from func.src.repositories.user.repository import UserRepository
from func.src.services.iara.service import SendToIara
from func.src.services.persephone.service import SendToPersephone
from func.src.transport.onboarding_steps.onboarding_steps_br import ValidateOnboardingStepsBR
from func.src.transport.onboarding_steps.onboarding_steps_us import ValidateOnboardingStepsUS


class UpdateMarketTimeExperience:
    @classmethod
    async def update_market_time_experience(
        cls,
        jwt_data: Jwt,
        time_experience_request: TimeExperienceRequest,
        device_info: DeviceInfo,
    ) -> bool:

        br_step_validator = ValidateOnboardingStepsBR.validate_onboarding_steps_br(
            jwt_data=jwt_data
        )
        us_step_validator = ValidateOnboardingStepsUS.validate_onboarding_steps_us(
            jwt_data=jwt_data
        )
        await asyncio.gather(br_step_validator, us_step_validator)

        await SendToPersephone.register_user_time_experience_log(
            jwt_data=jwt_data,
            time_experience_request=time_experience_request,
            device_info=device_info,
        )

        was_updated = await UserRepository.update_user_and_time_experience(
            unique_id=jwt_data.get_unique_id_from_jwt_payload(),
            time_experience_request=time_experience_request.time_experience,
        )
        if not was_updated:
            raise UniqueIdWasNotUpdate()

        await SendToIara.send_user_to_dw_registration(jwt_data=jwt_data)
        return was_updated
