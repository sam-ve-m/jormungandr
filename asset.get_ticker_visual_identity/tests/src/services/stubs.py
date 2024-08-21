# Jormungandr
from func.src.domain.validators.validator import Ticker


class StubTickerPayload:
    def __init__(self, symbol=None, region=None, type=None):
        self.symbol = symbol
        self.region = region
        self.type = type

    def to_dict(self):
        dict_params = {
            "symbol": self.symbol,
            "region": self.region,
            "type": self.type,
        }
        return dict_params


stub_ticker_path = "companies/BR/PETR/logo.png"
stub_url_access = (
    "https://dtvm-visual-identity-files.s3.amazonaws.com/companies/BR/PETR/logo.png"
)
stub_ticker_url_encoded = stub_url_access.encode()
stub_payload = StubTickerPayload(region="BR", symbol="PETR", type="logo").to_dict()
stub_payload_validated = Ticker(**stub_payload)
