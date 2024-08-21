import aiohttp
import orjson
from decouple import config
from etria_logger import Gladsheim


class OnboardingTransport:

    @classmethod
    async def get_us_onboarding_steps(cls, jwt) -> dict:
        try:
            url = f"{config('ONBOARDING_STEPS_BASE_URL')}/user/onboarding_user_current_step_us"
            current_omboarding_steps = await cls._execute_get_method(jwt=jwt, url=url)
            return current_omboarding_steps
        except Exception as e:
            Gladsheim.error(error=e, jwt=jwt, message="")

    @classmethod
    async def get_br_onboarding_steps(cls, jwt) -> dict:
        try:
            url = f"{config('ONBOARDING_STEPS_BASE_URL')}/user/onboarding_user_current_step_br"
            current_omboarding_steps = await cls._execute_get_method(jwt=jwt, url=url)
            return current_omboarding_steps
        except Exception as e:
            Gladsheim.error(error=e, jwt=jwt, message="")

    @classmethod
    async def _execute_get_method(cls, jwt, url) -> dict:
        headers = {
            "x-thebes-answer": jwt
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                print("Status:", response.status)
                print("Content-type:", response.headers['content-type'])

                body = await response.text()
                content = orjson.loads(body)
                return content
