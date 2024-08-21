from decouple import config
from etria_logger import Gladsheim

from func.src.domain.enums.file.extension import FileExtension
from func.src.domain.exceptions.model import ImageNotFound
from func.src.domain.models.request.model import BankVisualIdentityModel
from func.src.repositories.bank_visual_identity.repository import (
    BankVisualIdentityRepository,
)
from func.src.repositories.cache.repository import CacheRepository


class BankVisualIdentityService:
    __images_folder = config("BUCKET_IMAGES_FOLDER")

    @classmethod
    async def get_bank_logo(cls, bank_code: BankVisualIdentityModel):
        code = str(bank_code.bank_code)
        logo_url = await cls.__get_logo_url(code)
        return logo_url

    @classmethod
    def __get_logo_path(cls, bank_code: str) -> str:
        path = f"{cls.__images_folder}/{bank_code}/logo.{FileExtension.LOGO.value}"
        return path

    @classmethod
    async def __get_logo_url(cls, bank_code: str) -> str:
        cached_logo_url = CacheRepository.get_cached_logo(bank_code=bank_code)
        if cached_logo_url:
            return cached_logo_url

        logo_path = cls.__get_logo_path(bank_code)
        logo_exists = await BankVisualIdentityRepository.logo_exists(logo_path)
        if logo_exists:
            logo_url_access = await BankVisualIdentityRepository.generate_logo_url(
                logo_path
            )
            CacheRepository.save_logo_in_cache(
                logo_link=logo_url_access, bank_code=bank_code
            )
            return logo_url_access

        Gladsheim.error(message=f"No images found in this path: {logo_path}")
        raise ImageNotFound()
