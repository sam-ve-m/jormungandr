# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import request


# Jormungandr
from func.src.domain.enums import CodeResponse
from func.src.domain.exceptions import InvalidJwtToken
from func.src.domain.response import ResponseModel
from func.src.services.jwt import JwtService
from func.src.services.user import UserService
from func.src.services.onboarding import OnboardingStepService
from func.src.services.portfolio import PortfolioService


async def get_user_snapshot():
    jwt = None
    try:
        jwt = request.headers["x-thebes-answer"]
        jwt_content = await JwtService.get_valid_jwt_content(jwt=jwt)
        unique_id = jwt_content.get("user").get("unique_id")
        if not unique_id:
            raise InvalidJwtToken("Invalid jwt content")

        user_personal_data = await UserService.get_user_data(unique_id=unique_id)
        onboarding_steps = await OnboardingStepService.get_current_user_current_onboaridng_progress(jwt=jwt)
        portfolios = await PortfolioService.get_user_portfolio(unique_id=unique_id)

        snapshots = {
            "token_content": jwt_content,
            "onboarding_steps": onboarding_steps,
            "portfolio": portfolios,
            "user": user_personal_data
        }

        response_model = ResponseModel.build_response(result=snapshots, code=CodeResponse.SUCCESS)
        response = ResponseModel.build_http_response(response_model=response_model, status=HTTPStatus.OK)
        return response

    except InvalidJwtToken as ex:
        Gladsheim.error(error=ex, jwt=jwt)
        response_model = ResponseModel.build_error_response(code=CodeResponse.JWT_INVALID, message=ex.msg)
        response = ResponseModel.build_http_response(response_model=response_model, status=HTTPStatus.UNAUTHORIZED)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response_model = ResponseModel.build_error_response(
            code=CodeResponse.INTERNAL_SERVER_ERROR,
            message="Unexpected error occurred",
        )
        response = ResponseModel.build_http_response(
            response_model=response_model,
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
        return response
