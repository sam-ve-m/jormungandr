from pydantic import BaseModel

from func.src.domain.models.device_info.model import DeviceInfo


class TimeExperienceRequest(BaseModel):
    time_experience: str


class TimeExperienceTemplates:
    @classmethod
    def user_time_experience_schema_template(
        cls, time_experience: str, unique_id: str, device_info: DeviceInfo
    ) -> dict:
        time_experience_template = {
            "unique_id": unique_id,
            "time_experience": time_experience,
            "device_info": device_info.device_info,
            "device_id": device_info.device_id,
        }
        return time_experience_template
