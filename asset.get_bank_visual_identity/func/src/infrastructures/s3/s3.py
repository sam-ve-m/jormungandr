from boto3 import resource
from decouple import config
from etria_logger import Gladsheim


class S3Infrastructure:
    __access_key_id = config("AWS_ACCESS_KEY_ID")
    __secret_access_key = config("AWS_SECRET_ACCESS_KEY")
    __region_name = config("AWS_REGION_NAME")

    @classmethod
    async def get_resource(cls):
        try:
            s3_resource = resource(
                "s3",
                aws_access_key_id=cls.__access_key_id,
                aws_secret_access_key=cls.__secret_access_key,
                region_name=cls.__region_name,
            )
            return s3_resource

        except Exception as ex:
            Gladsheim.error(error=ex, message="Error trying to get s3 resource")
            raise ex

    @staticmethod
    async def get_bucket(bucket_name: str):
        s3_resource = await S3Infrastructure.get_resource()
        bucket = s3_resource.Bucket(bucket_name)
        return bucket
