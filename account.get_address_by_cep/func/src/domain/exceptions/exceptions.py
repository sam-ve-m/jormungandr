class ErrorRequestingEnum(Exception):
    msg = "Fail in making http request to enums"


class StateEnumNotFound(Exception):
    msg = "Given state does not exists in enum"


class CityEnumNotFound(Exception):
    msg = "Given city does not exists in enum"
