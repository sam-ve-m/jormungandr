from func.src.services.user_register import UserService
from tests.src.services.stubs import stub_payload_validated, stub_device_info


# Third party
from pytest import fixture


@fixture(scope="function")
def user_service():
    setup_service_instance = UserService(
        payload_validated=stub_payload_validated, device_info=stub_device_info
    )
    yield setup_service_instance
