from ...services.user.service import UserService


class PortfolioService:
    @classmethod
    async def get_user_portfolio(cls, unique_id: str) -> dict:
        user_portfolios = await UserService.get_user_portfolios_ids(unique_id=unique_id)
        br_wallet_id = cls._find_wallet_id_br(user_portfolios)
        br_wallet = cls._request_wallet_br(br_wallet_id)
        us_wallet_id = cls._find_wallet_id_us(user_portfolios)
        us_wallet = cls._request_wallet_us(us_wallet_id)
        vnc_br_wallets_ids = cls._find_wallets_ids_vnc_br(user_portfolios)
        vnc_br_wallets = {wallet_id: cls._request_wallet_vai_na_cola_br(wallet_id) for wallet_id in vnc_br_wallets_ids}
        return {
            "wallet_id_br": br_wallet_id,
            "wallet_br": br_wallet,
            "wallet_id_us": us_wallet_id,
            "wallet_us": us_wallet,
            "wallets_vnc_br": vnc_br_wallets,
        }

    @staticmethod
    def _find_wallet_id_br(user_data) -> str:
        wallet_id = user_data.get('portfolios', {}).get('default', {}).get("br")
        return wallet_id

    @staticmethod
    def _find_wallet_id_us(user_data) -> str:
        wallet_id = user_data.get('portfolios', {}).get('default', {}).get("us")
        return wallet_id

    @staticmethod
    def _find_wallets_ids_vnc_br(user_data) -> tuple:
        wallets_ids = tuple(
            wallet.get("bovespa_account")
            for wallet in user_data.get('portfolios', {}).get('vnc', {}).get('br', [])
        )
        return wallets_ids

    @staticmethod
    def _request_wallet_br(wallet_id: str) -> list:
        return []

    @staticmethod
    def _request_wallet_us(wallet_id: str) -> list:
        return []

    @staticmethod
    def _request_wallet_vai_na_cola_br(wallet_id: str) -> list:
        return []
