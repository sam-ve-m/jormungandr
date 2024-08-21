import datetime

stub_unique_id = "40db7fee-6d60-4d73-824f-1bf87edc4491"
stub_user = {
    "nick_name": "RAST3",
    "email": "abc1@lionx.com.br",
    "unique_id": "451baf5a-9cd5-4037-aa17-fbd0fcef66c8",
    "created_at": datetime.datetime(2022, 3, 2, 11, 36, 8, 672000),
    "scope": {"view_type": "default", "features": ["default", "realtime"]},
    "is_active_user": True,
    "must_do_first_login": False,
    "use_magic_link": True,
    "token_valid_after": datetime.datetime(2022, 3, 2, 11, 36, 8, 672000),
    "terms": {
        "term_application": None,
        "term_open_account": None,
        "term_retail_liquid_provider": None,
        "term_refusal": {
            "version": 3,
            "date": datetime.datetime(2022, 3, 2, 11, 36, 57, 922000),
            "is_deprecated": False,
        },
        "term_non_compliance": None,
    },
    "suitability": {
        "score": 1.0,
        "submission_date": datetime.datetime(2022, 3, 2, 11, 37, 12, 885000),
        "suitability_version": 2,
    },
    "identifier_document": {
        "cpf": "62499511303",
        "document_data": {
            "type": "RG",
            "number": "385722594",
            "date": datetime.datetime(2019, 3, 17, 21, 0),
            "issuer": "SSP",
            "state": "SP",
        },
    },
    "phone": "11987450574",
    "tax_residences": [
        {"country": "AUT", "tax_number": "1212-012"},
        {"country": "CHE", "tax_number": "1212-012"},
    ],
    "bureau_status": "approved",
    "is_bureau_data_validated": True,
    "marital": {
        "status": 1,
        "spouse": {"name": "fulana", "cpf": "1234567890", "nationality": 5},
    },
    "address": {
        "country": "BRA",
        "street_name": "RUA IMBUIA",
        "city": 5150,
        "number": 153,
        "zip_code": "06184110",
        "neighborhood": "CIDADE DAS FLORES",
        "state": "SP",
    },
    "assets": {
        "patrimony": 200000.0,
        "income": 200000.0,
        "date": datetime.datetime(2022, 3, 2, 0, 0, 0, 803000),
    },
    "birth_date": datetime.datetime(1993, 10, 9, 0, 0),
    "birth_place_city": 5150,
    "birth_place_country": "BRA",
    "birth_place_state": "SP",
    "father_name": "Arge Ferreira",
    "gender": "M",
    "mother_name": "Vani Silva",
    "name": "Teste Almeida",
    "nationality": 1,
    "occupation": {
        "activity": 399,
        "company": {"cnpj": "36923006000188", "name": "LionX"},
    },
    "can_be_managed_by_third_party_operator": False,
    "is_active_client": True,
    "is_managed_by_third_party_operator": False,
    "last_modified_date": {
        "concluded_at": datetime.datetime(2022, 3, 2, 11, 38, 15, 889000)
    },
    "portfolios": {
        "default": {"br": {"bovespa_account": "000000037-5", "bmf_account": "37"}},
        "vnc": {"br": []},
    },
    "sinacor": True,
    "sincad": False,
    "solutiontech": "send",
    "third_party_operator": {
        "is_third_party_operator": False,
        "details": {},
        "third_party_operator_email": "string",
    },
    "electronic_signature": "ea73ced01f94d96f7f46682055d6e3915b626a2ebbf98818a09ea2efb6af1a9e",
    "electronic_signature_wrong_attempts": 0,
    "is_blocked_electronic_signature": False,
}
