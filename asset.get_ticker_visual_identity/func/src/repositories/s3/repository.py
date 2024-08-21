# Jormungandr
from ...infrastructures.s3.infrastructure import S3Infrastructure

# Third party
from decouple import config


class S3Repository:
    @staticmethod
    async def get_ticker(ticker_path: str) -> bool:
        async with S3Infrastructure.get_resource() as s3_resource:
            bucket = await s3_resource.Bucket(config("AWS_BUCKET_NAME"))
            ticker = [
                ticker async for ticker in bucket.objects.filter(Prefix=ticker_path)
            ]
        return bool(ticker)

    @staticmethod
    async def generate_ticker_url(ticker_path: str) -> str:
        async with S3Infrastructure.get_resource() as s3_resource:
            ticker_url = await s3_resource.meta.client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": config("AWS_BUCKET_NAME"), "Key": ticker_path},
                ExpiresIn=3600,
            )
        return ticker_url
