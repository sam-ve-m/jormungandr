# Jormungandr
from ...domain.models.suitability.model import SuitabilityModel, SuitabilityValidator
from ...repositories.mongo_db.suitability.repository import SuitabilityRepository

# Third party
from mnemosine import AsyncCache
from decouple import config


class SuitabilityService:
    @staticmethod
    async def get_latest_questions_with_answer_options():
        suitability = await AsyncCache.get(key=config("REDIS_SUITABILITY_KEY"))
        if not suitability:
            suitability = await SuitabilityRepository.get_latest_suitability()
            await AsyncCache.save(
                key=config("REDIS_SUITABILITY_KEY"),
                value=suitability,
                time_to_live=int(config("REDIS_TIME_TO_LIVE")),
            )
        suitability_validated = SuitabilityValidator(**suitability)
        suitability_model = SuitabilityModel(suitability=suitability_validated)
        response_template = suitability_model.get_suitability_response_template()
        return response_template
