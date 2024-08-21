# Jormungandr
from .repository import RedisRepository
from .exceptions import ErrorToRequestZendeskApi, InvalidEndpointZendeskApi

# Standards
from http import HTTPStatus

# Third Party
from decouple import config
from etria_logger import Gladsheim
import requests


def get_all_custom_fields() -> dict:
    redis_custom_fields = RedisRepository.get()
    if redis_custom_fields:
        decoded_custom_fields = redis_custom_fields.decode()
        ticket_custom_fields = eval(decoded_custom_fields)
        return ticket_custom_fields
    zendesk_ticket_custom_fields = __request_zendesk_custom_fields()
    ticket_custom_fields = __treatment_ticket_custom_fields(
        zendesk_ticket_custom_fields
    )
    RedisRepository.set(ticket_custom_fields)
    return ticket_custom_fields


def __request_zendesk_custom_fields() -> dict:
    try:
        zendesk_ticket_custom_fields = requests.get(
            config("ZENDESK_TICKET_CUSTOM_FIELDS_API_URL"),
            auth=(config("ZENDESK_LOGIN"), config("ZENDESK_PASSWORD")),
        )
        status_code = zendesk_ticket_custom_fields.status_code
    except Exception as ex:
        message = (
            f"Jormungandr::get_all_custom_fields::__request_zendesk_custom_fields:: error to get zendesk custom"
            f"fields"
        )
        Gladsheim.error(error=ex, message=message)
        raise ErrorToRequestZendeskApi
    if status_code == HTTPStatus.OK:
        return zendesk_ticket_custom_fields.json()
    raise InvalidEndpointZendeskApi


def __treatment_ticket_custom_fields(ticket_custom_fields: dict) -> dict:
    ticket_custom_fields_treatment = {"custom_fields": []}
    for field in ticket_custom_fields["ticket_fields"]:
        custom_field_options = field.get("custom_field_options", False)
        if custom_field_options:
            options = [
                {"id": option["id"], "name": option["name"], "value": option["value"]}
                for option in custom_field_options
            ]
            treatment_custom_field = dict()
            treatment_custom_field.update(id=field["id"])
            treatment_custom_field.update(title=field["title"])
            treatment_custom_field.update(custom_field_options=options)
            ticket_custom_fields_treatment["custom_fields"].append(treatment_custom_field)
    return ticket_custom_fields_treatment
