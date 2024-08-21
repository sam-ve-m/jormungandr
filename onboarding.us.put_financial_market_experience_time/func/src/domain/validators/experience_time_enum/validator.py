# PROJECT IMPORTS
from func.src.domain.exceptions.exceptions import EnumSentIsNotaValidEnum


class ValidateEnumFromRequest:
    @classmethod
    def check_validity_experience_time_enum(
        cls, enums_dict: dict, time_experience_model: str
    ) -> bool:

        enum_is_valid = time_experience_model in enums_dict

        if not enum_is_valid:
            raise EnumSentIsNotaValidEnum()

        return bool(enum_is_valid)
