import aiohttp


class HttpInfrastructure:
    session = None

    @classmethod
    def get_session(cls) -> aiohttp.ClientSession:
        if cls.session is None:
            cls.session = aiohttp.ClientSession()
        return cls.session
