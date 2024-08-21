# Jormungandr
from ..enums.regions import RegionOptions
from ..validators.validator import Ticker

# Third party
from decouple import config


class TickerModel:
    def __init__(self, payload_validated: Ticker):
        self.region = payload_validated.region
        self.ticker_type = payload_validated.type
        self.symbol = self._treatment_ticker_symbol(
            symbol=payload_validated.symbol, region=payload_validated.region
        )

    @staticmethod
    def _treatment_ticker_symbol(symbol: str, region: RegionOptions):
        if region == RegionOptions.BR:
            ticker_slice_index = int(config("TICKER_SLICE_INDEX"))
            return symbol[:ticker_slice_index]
        return symbol

    async def get_ticker_path_by_type(self) -> str:
        initial_path = config("INITIAL_PATH")
        url_per_type = {
            "logo": f'{initial_path}/{self.region}/{self.symbol}/{self.ticker_type}.{config("LOGO_EXTENSION")}',
            "banner": f'{initial_path}/{self.region}/{self.symbol}/{self.ticker_type}.{config("BANNER_EXTENSION")}',
            "thumbnail": f'{initial_path}/{self.region}/{self.symbol}/{self.ticker_type}.{config("THUMBNAIL_EXTENSION")}',
        }
        url_path = url_per_type.get(self.ticker_type)
        return url_path

    async def get_result_template(self, ticker_url_access: str) -> dict:
        result = {"url": ticker_url_access, "type": self.ticker_type}
        return result
