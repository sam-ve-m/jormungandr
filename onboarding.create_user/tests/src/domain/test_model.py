# Jormungandr - Onboarding
from tests.src.services.stubs import stub_user_model


def test_when_init_model_then_return_expected_values():
    assert stub_user_model.is_active_user is False
    assert stub_user_model.email_validated is False
    assert stub_user_model.must_to_first_login is True
