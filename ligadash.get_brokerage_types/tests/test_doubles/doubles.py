# Doubles of: main

main_service_response_dummy = '{"result": [{"code": 1, "value": "BRASILEIRO NATO"}, {"code": 2, "value": "BRASILEIRO NATURALIZADO"}, {"code": 3, "value": "ESTRANGEIRO"}], "message": null, "success": true, "code": 0}'
main_response_dummy = main_service_response_dummy.encode()

# Doubles of: src.service.enum.service

enum_service_get_enums_response_ok = [(1, "Enum"), (2, "Enum2"), (3, "Enum3")]
enum_service_response_ok = '{"result": [{"code": 1, "value": "Enum"}, {"code": 2, "value": "Enum2"}, {"code": 3, "value": "Enum3"}], "message": null, "success": true, "code": 0}'
enum_service_get_enums_response_none = None
enum_service_response_none = '{"result": [], "message": "Data not found or inconsistent.", "success": false, "code": 99}'
enum_service_get_enums_response_invalid = [(1)]
enum_service_response_invalid = '{"result": [], "message": "Error trying to get the enum.", "success": false, "code": 99}'

# Doubles of: src.repository.enum.repository

enum_repository_get_cached_enum_dummy = [(1, "Enum"), (2, "Enum2"), (3, "Enum3")]
enum_repository_get_from_cache_dummy_none = None
enum_repository_get_from_cache_dummy_list = [(1, "Enum"), (2, "Enum2"), (3, "Enum3")]
enum_repository_query_dummy = [(1, "Enum"), (2, "Enum2"), (3, "Enum3")]
enum_repository_save_in_cache_dummy = True
