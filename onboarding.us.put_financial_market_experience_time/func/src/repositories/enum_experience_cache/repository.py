# STANDARD IMPORTS
from typing import Union

# THIRD PART IMPORTS
from etria_logger import Gladsheim
from mnemosine import SyncCache


class EnumExperienceTimeCacheRepository:
    enum_key = "jormungandr:onboarding:EnumExperienceTime"

    @classmethod
    def save_enum_experience_time(
        cls, enum_experience_time: list, time: int = 3600
    ) -> bool:
        try:
            SyncCache.save(cls.enum_key, list(enum_experience_time), int(time))
            return True
        except ValueError as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            return False
        except TypeError as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            return False
        except Exception as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            return False

    @classmethod
    def get_enum_experience_time(cls) -> Union[list, None]:
        result = SyncCache.get(cls.enum_key)
        return result
