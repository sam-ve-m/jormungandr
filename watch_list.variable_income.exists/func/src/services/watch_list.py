from func.src.domain.request.model import WatchListSymbol
from func.src.domain.watch_list.model import WatchListSymbolModel
from func.src.repositories.watch_list.repository import WatchListRepository


class WatchListService:
    @classmethod
    async def symbol_exists(cls, watch_list_symbol: WatchListSymbol, unique_id: str):
        symbol = WatchListSymbolModel(watch_list_symbol, unique_id)
        exists = await WatchListRepository.exists(symbol)

        service_result = {"is_symbol_in_watchlist": exists}

        return service_result
