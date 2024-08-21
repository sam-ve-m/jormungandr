# Jormungandr - Onboarding
from func.src.services.builder.customer_registration import CustomerRegistrationBuilder
from tests.src.services.builder.stubs import stub_user_data


def test_when_have_spouse_then_have_expected_spouse_name():
    customer_user_registration = CustomerRegistrationBuilder(
        user_data=stub_user_data
    ).build()
    assert bool(
        customer_user_registration.get("marital").get("spouse").get("spouse_name")
    )


def test_when_have_spouse_then_have_expected_spouse_cpf():
    customer_user_registration = CustomerRegistrationBuilder(
        user_data=stub_user_data
    ).build()
    assert bool(
        customer_user_registration.get("marital").get("spouse").get("spouse_cpf")
    )


def test_when_have_spouse_then_have_expected_spouse_nationality():
    customer_user_registration = CustomerRegistrationBuilder(
        user_data=stub_user_data
    ).build()
    assert bool(
        customer_user_registration.get("marital").get("spouse").get("nationality")
    )


def test_when_have_spouse_then_not_have_expected_values():
    customer_user_registration = CustomerRegistrationBuilder(user_data={}).build()
    assert not customer_user_registration.get("marital").get("spouse")
