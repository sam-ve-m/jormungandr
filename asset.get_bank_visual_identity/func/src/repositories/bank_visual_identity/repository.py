from decouple import config

from func.src.core.interfaces.repositories.bank_visual_identity.interface import (
    IBankVisualIdentityRepository,
)
from func.src.infrastructures.s3.s3 import S3Infrastructure


class BankVisualIdentityRepository(IBankVisualIdentityRepository):
    link_expiration_time = config("LINK_EXPIRATION_TIME_IN_SECONDS")
    bucket_name = config("AWS_BUCKET_NAME")

    @classmethod
    async def logo_exists(cls, logo_path: str) -> bool:
        bucket = await S3Infrastructure.get_bucket(cls.bucket_name)
        result = list(bucket.objects.filter(Prefix=logo_path))
        return bool(result)

    @classmethod
    async def generate_logo_url(cls, logo_path: str) -> str:
        s3_resource = await S3Infrastructure.get_resource()
        logo_url = s3_resource.meta.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": cls.bucket_name, "Key": logo_path},
            ExpiresIn=cls.link_expiration_time,
        )
        return logo_url
