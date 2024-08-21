# Jormungandr
from ..domain.exceptions.exception import TickerNotFound
from ..domain.ticker.model import TickerModel
from ..domain.validators.validator import Ticker
from ..repositories.s3.repository import S3Repository
from ..repositories.redis.repository import RedisRepository


class TickerVisualIdentityService:
    @staticmethod
    async def get_ticker_url(payload_validated: Ticker) -> dict:
        ticker_model = TickerModel(payload_validated=payload_validated)
        ticker_path = await ticker_model.get_ticker_path_by_type()
        ticker_url_access = (
            await TickerVisualIdentityService._get_or_set_ticker_url_access(
                ticker_path=ticker_path
            )
        )
        result = await ticker_model.get_result_template(
            ticker_url_access=ticker_url_access
        )
        return result

    @staticmethod
    async def _get_or_set_ticker_url_access(ticker_path: str) -> str:
        result = await RedisRepository.get(ticker_path)
        if result:
            ticker_url_access = result.decode()
            return ticker_url_access
        ticker_exist = await S3Repository.get_ticker(ticker_path=ticker_path)
        if not ticker_exist:
            raise TickerNotFound
        ticker_url_access = await S3Repository.generate_ticker_url(
            ticker_path=ticker_path
        )
        await RedisRepository.set(key=ticker_path, value=ticker_url_access)
        return ticker_url_access
