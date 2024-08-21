import asyncio

from ...transports.onboarding import OnboardingTransport


class OnboardingStepService:
    transport = OnboardingTransport

    @classmethod
    async def get_current_user_current_onboaridng_progress(cls, jwt) -> dict:
        onboarding_progress_by_country = {
            "br": cls.transport.get_br_onboarding_steps,
            "us": cls.transport.get_us_onboarding_steps,
        }
        futures = [
            onboarding_progress_callback(jwt=jwt)
            for country, onboarding_progress_callback in onboarding_progress_by_country.items()
        ]
        responses = await asyncio.gather(*futures)

        onboaridng_progress = {
            country: responses[_index]
            for _index, country in enumerate(onboarding_progress_by_country)
        }

        return onboaridng_progress
