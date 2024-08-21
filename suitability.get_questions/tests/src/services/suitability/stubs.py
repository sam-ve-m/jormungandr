# Jormungandr
from func.src.domain.models.suitability.model import SuitabilityModel
from func.src.domain.validators.suitability.validator import SuitabilityValidator

# Third party
import datetime

stub_suitability_mongo_db = {
    "_id": "6339bfa7d6d9c4f5440e6328",
    "questions": [
        {
            "order_id": 1,
            "weight": 14,
            "text": "Primeira pergunta",
            "answers": [
                {"text": "resposta1", "option_id": 1, "weight": 5},
                {"text": "resposta2", "option_id": 2, "weight": 5},
                {"text": "resposta3", "option_id": 3, "weight": 2},
                {"text": "resposta4", "option_id": 4, "weight": 8},
            ],
        },
        {
            "order_id": 2,
            "weight": 10,
            "text": "Segunda pergunta",
            "answers": [
                {"text": "resposta1", "option_id": 1, "weight": 2},
                {"text": "resposta2", "option_id": 2, "weight": 5},
                {"text": "resposta3", "option_id": 3, "weight": 7},
                {"text": "resposta4", "option_id": 4, "weight": 4},
            ],
        },
        {
            "order_id": 3,
            "weight": 14,
            "text": "Terceira pergunta",
            "answers": [
                {"text": "resposta1", "option_id": 1, "weight": 5},
                {"text": "resposta2", "option_id": 2, "weight": 6},
                {"text": "resposta3", "option_id": 3, "weight": 7},
            ],
        },
        {
            "order_id": 4,
            "weight": 11,
            "text": "Segunda pergunta",
            "answers": [
                {"text": "resposta1", "option_id": 1, "weight": 3},
                {"text": "resposta2", "option_id": 2, "weight": 2},
                {"text": "resposta3", "option_id": 3, "weight": 6},
                {"text": "resposta4", "option_id": 4, "weight": 4},
            ],
        },
    ],
    "date": datetime.datetime(2022, 10, 2, 13, 43, 19, 477000),
    "version": 12,
}
stub_suitability_validated = SuitabilityValidator(**stub_suitability_mongo_db)
stub_suitability_model = SuitabilityModel(suitability=stub_suitability_validated)
stub_response = stub_suitability_model.get_suitability_response_template()
