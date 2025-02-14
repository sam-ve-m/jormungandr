from func.src.domain.request.model import WatchListSymbols
from func.src.domain.watch_list.model import WatchListSymbolModel
from func.src.repositories.watch_list.repository import WatchListRepository


class WatchListService:
    @classmethod
    async def register_symbols(
        cls, watch_list_symbols: WatchListSymbols, unique_id: str
    ):
        symbols_list = [
            WatchListSymbolModel(symbol, unique_id)
            for symbol in watch_list_symbols.symbols
        ]
        await WatchListRepository.insert_all_symbols_in_watch_list(symbols_list)
        return True
