# Third party
from etria_logger import Gladsheim
from flask import Response

# Standards
from http import HTTPStatus
from json import dumps

# Jormungandr
from src.service import get_all_custom_fields
from src.exceptions import InvalidEndpointZendeskApi, ErrorToRequestZendeskApi
from src.enum import CodeResponse


def get_all_ticket_custom_fields():
    message = "Jormungandr::get_all_ticket_custom_fields"
    try:
        service_response = get_all_custom_fields()
        response = Response(
            dumps(
                {
                    "result": service_response,
                    "message": None,
                    "success": True,
                    "code": CodeResponse.SUCCESS.value,
                }
            ),
            mimetype="application/json",
            status=HTTPStatus.OK,
        )
        return response

    except InvalidEndpointZendeskApi as ex:
        Gladsheim.error(ex, f"{message}::Invalid endpoint for Zendesk Api.")
        response = Response(
            dumps(
                {
                    "result": None,
                    "message": ex.msg,
                    "success": False,
                    "code": CodeResponse.INVALID_ZENDESK_API_URL.value,
                }
            ),
            mimetype="application/json",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
        return response

    except ErrorToRequestZendeskApi as ex:
        Gladsheim.error(ex, f"{message}::Failed to request ticket custom fields to Zendesk Api.")
        response = Response(
            dumps(
                {
                    "result": None,
                    "message": ex.msg,
                    "success": False,
                    "code": CodeResponse.ERROR_TO_REQUEST_ZENDESK_API.value,
                }
            ),
            mimetype="application/json",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
        return response

    except Exception as ex:
        Gladsheim.error(ex, f"{message}::{str(ex)}")
        response = Response(
            dumps(
                {
                    "result": None,
                    "message": "Unexpected error occurred",
                    "success": False,
                    "code": CodeResponse.INTERNAL_SERVER_ERROR.value,
                }
            ),
            mimetype="application/json",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
        return response
