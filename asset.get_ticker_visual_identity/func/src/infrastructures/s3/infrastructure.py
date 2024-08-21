# Third party
from aioboto3 import Session
from contextlib import asynccontextmanager
from decouple import config
from etria_logger import Gladsheim


class S3Infrastructure:
    session = None

    @classmethod
    async def _get_session(cls):
        if cls.session is None:
            try:
                cls.session = Session(
                    aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
                    region_name=config("AWS_REGION_NAME"),
                )

            except Exception as ex:
                Gladsheim.error(error=ex, message="Error trying to get aws session")
                raise ex
        return cls.session

    @classmethod
    @asynccontextmanager
    async def get_resource(cls):
        session = await S3Infrastructure._get_session()
        try:
            async with session.resource("s3") as s3_resource:
                yield s3_resource
        except Exception as ex:
            Gladsheim.error(error=ex, message="Error trying to get s3 resource")
            raise ex
