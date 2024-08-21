# Jormungandr - Onboarding
from .builder.customer_registration import CustomerRegistrationBuilder
from ..domain.exceptions.exceptions import UserUniqueIdNotExists
from ..repositories.mongo_db.user.repository import UserRepository


class UserDataService:
    @staticmethod
    async def get_registration_data(unique_id: str) -> dict:
        user_data = await UserRepository.find_one_by_unique_id(unique_id=unique_id)
        if not user_data:
            raise UserUniqueIdNotExists
        customer_registration_data_built = CustomerRegistrationBuilder(
            user_data=user_data
        ).build()
        return customer_registration_data_built
