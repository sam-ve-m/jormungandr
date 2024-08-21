from ...domain.exceptions import UserNotFound
from ...repository.user.repository import UserRepository


class UserService:
    @staticmethod
    async def get_user_data(unique_id: str) -> dict:
        user_data = await UserRepository.find_user_by_unique_id(
            unique_id=unique_id,
            projection={
                "email": 1,
                "name": 1,
                "nick_name": 1,
                "suitability": 1,
                "identifier_document": 1,
                "cel_phone": 1,
                "tax_residences": 1,
                "marital": 1,
                "person_type": 1,
                "address": 1,
                "birthplace": 1,
                "assets": 1,
                "birth_date": 1,
                "mother_name": 1,
                "nationality": 1,
                "occupation": 1,
                "sinacor": 1,
                "sincad": 1,
                "solutiontech": 1,
                "dw": 1,
                "bank_accounts": 1,
            }
        )
        if not user_data:
            raise UserNotFound("Unable to find user")
        return user_data

    @staticmethod
    async def get_user_portfolios_ids(unique_id: str) -> dict:
        user_data = await UserRepository.find_user_by_unique_id(unique_id=unique_id, projection={"portfolios": 1})
        if not user_data:
            raise UserNotFound("Unable to find user")
        return user_data
