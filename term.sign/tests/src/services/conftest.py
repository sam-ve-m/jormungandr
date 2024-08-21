from pytest import fixture

from func.src.services.terms import TermSignService
from .stubs import stub_terms_type_validated, stub_unique_id, stub_device_info


@fixture(scope="function")
def term_sign_service():
    service_instance = TermSignService(
        unique_id=stub_unique_id,
        terms_type_validated=stub_terms_type_validated,
        device_info=stub_device_info,
    )
    return service_instance
