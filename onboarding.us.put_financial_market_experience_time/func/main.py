from http import HTTPStatus

from etria_logger import Gladsheim
from flask import request, Response, Request

from func.src.domain.enums.status_code.enum import InternalCode
from func.src.domain.exceptions.exceptions import (
    ErrorOnDecodeJwt,
    NotSentToPersephone,
    UniqueIdWasNotUpdate,
    InvalidOnboardingStep,
    TransportOnboardingError,
    UserWasNotFound,
    EnumSentIsNotaValidEnum,
    ErrorLoggingOnIara,
    DeviceInfoRequestFailed,
    DeviceInfoNotSupplied,
)
from func.src.domain.models.jwt.models import Jwt
from func.src.domain.models.response.model import ResponseModel
from func.src.domain.models.time_experience.model import TimeExperienceRequest
from func.src.services.enum_experience_time.service import ExperienceTimeEnumService
from func.src.services.update_time_experience.service import UpdateMarketTimeExperience
from func.src.transport.device_info.transport import DeviceSecurity


async def update_experience_time(request: Request = request) -> Response:
    try:
        x_thebes_answer = request.headers.get("x-thebes-answer")
        x_device_info = request.headers.get("x-device-info")
        request_body = request.json

        jwt_data = Jwt(jwt=x_thebes_answer)
        await jwt_data()
        device_info = await DeviceSecurity.get_device_info(x_device_info)
        time_experience_request = TimeExperienceRequest(**request_body)

        ExperienceTimeEnumService.experience_time_enum_validation(
            time_experience_model=time_experience_request
        )
        service_response = (
            await UpdateMarketTimeExperience.update_market_time_experience(
                jwt_data=jwt_data,
                time_experience_request=time_experience_request,
                device_info=device_info,
            )
        )

        response = ResponseModel(
            success=True,
            code=InternalCode.SUCCESS,
            message="The Time Experience of Financial Market Was Updated Successfully",
            result=service_response,
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except InvalidOnboardingStep as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="User in invalid onboarding step",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ErrorOnDecodeJwt as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message="Error On Decoding JWT",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except TransportOnboardingError as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.TRANSPORT_ON_BOARDING_ERROR,
            message="ValidateOnboardingSteps::validate_onboarding_steps::Error trying to verify the onboarding step",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except NotSentToPersephone as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.NOT_SENT_TO_PERSEPHONE,
            message="Not Sent to Persephone",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except UserWasNotFound as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.USER_WAS_NOT_FOUND,
            message="User Not Found",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except UniqueIdWasNotUpdate as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.UNIQUE_ID_WAS_NOT_UPDATED,
            message="Unique Id Was Not Updated",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except EnumSentIsNotaValidEnum as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.NOT_A_VALID_ENUM,
            message="ValidateEnumFromRequest.check_validity_experience_time_enum::This is not a valid enum",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except ErrorLoggingOnIara as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.ERROR_LOGGIN_ON_IARA,
            message="Error Logging On Iara",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except DeviceInfoRequestFailed as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Error trying to get device info",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except DeviceInfoNotSupplied as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="Device info not supplied",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Unexpected error occurred",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
