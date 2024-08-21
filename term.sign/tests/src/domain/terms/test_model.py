from tests.src.services.stubs import stub_terms_model


def test_when_get_term_sign_then_return_expected_values():
    result = stub_terms_model._get_term_and_sign()

    assert result.get("terms.term_application").get("is_deprecated") is False
