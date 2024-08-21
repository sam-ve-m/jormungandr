from func.src.domain.validators.validator import TermFiles
from ..domain.exceptions.exceptions import (
    UserUniqueIdNotExists,
    TermVersionNotExists,
    ErrorOnUpdateUser,
)
from ..domain.models.device_info import DeviceInfo
from ..domain.terms.model import TermsModel
from ..repositories.mongo_db.user.repository import UserRepository
from ..repositories.s3.repository import FileRepository
from ..transports.audit.transport import Audit


class TermSignService:
    def __init__(
        self, unique_id: str, terms_type_validated: TermFiles, device_info: DeviceInfo
    ):
        self.unique_id = unique_id
        self.terms_type_validated = terms_type_validated
        self.device_info = device_info

    async def user_terms_sign(self) -> bool:
        terms_version = await self._get_terms_version()
        terms_model = TermsModel(
            unique_id=self.unique_id,
            terms_version=terms_version,
            terms_type_validated=self.terms_type_validated,
            device_info=self.device_info,
        )
        await Audit.record_message_log(terms_model=terms_model)
        user_updated = await UserRepository.update_one_with_terms_signed(
            unique_id=self.unique_id, terms_signed=terms_model.terms_signed
        )
        if not user_updated.matched_count:
            raise ErrorOnUpdateUser()
        return True

    async def _get_terms_version(self) -> list:
        terms_version = list()
        for term_type in self.terms_type_validated.terms_file:
            term_version = await FileRepository.get_current_term_version(
                term_type=term_type
            )
            if not term_version:
                raise TermVersionNotExists()
            terms_version.append(term_version)
        return terms_version

    async def _verify_unique_id_exists(self) -> bool:
        user = await UserRepository.find_one_by_unique_id(unique_id=self.unique_id)
        if not user:
            raise UserUniqueIdNotExists()
        return True
