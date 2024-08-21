# Term
from func.src.domain.exceptions.services.exception import ErrorToGenerateOrderToken
from func.src.services.order_token.service import OrderToken
from tests.src.services.order_token.stubs import term_with_order, stub_unique_id


# Standards
from unittest.mock import patch

# Third party
import pytest


@pytest.mark.asyncio
@patch("func.src.services.order_token.service.Harpocrates.generate_jwt", return_value=("jwt_token", 0))
async def test_when_generate_token_with_successfully_then_return_expected_values(mock_harpocrates):
    result = await OrderToken.generate_token(jwt_content={"teste": "teste"})

    assert isinstance(result, str)


@pytest.mark.asyncio
@patch("func.src.services.order_token.service.Harpocrates.generate_jwt", return_value=("jwt_token", 1))
async def test_when_failed_to_generate_token_then_return_raises(mock_harpocrates):
    with pytest.raises(ErrorToGenerateOrderToken):
        await OrderToken.generate_token(jwt_content={"teste": "teste"})


@pytest.mark.asyncio
@patch("func.src.services.order_token.service.OrderToken.generate_token", return_value="token123")
@patch("func.src.services.order_token.service.TermTransport.sign_term")
async def test_when_sign_term_and_generate_token_with_successfully_then_return_order_token(mock_term_sign, mock_generate_token):
    result = await OrderToken.sign_term_and_generate_order_token(term_with_order=term_with_order, jwt="123", unique_id=stub_unique_id)

    assert isinstance(result, str)
    assert result == "token123"
