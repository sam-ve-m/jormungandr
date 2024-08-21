from func.src.domain.models.device_info import DeviceInfo
from func.src.domain.terms.model import TermsModel
from func.src.domain.validators.validator import TermFiles


class UserUpdated:
    def __init__(self, matched_count=None):
        self.matched_count = matched_count


stub_user_not_updated = UserUpdated(matched_count=False)
stub_user_updated = UserUpdated(matched_count=True)
stub_terms_file = {
    "terms_file": ["term_application", "term_open_account", "term_non_compliance"]
}
stub_unique_id = "40db7fee-6d60-4d73-824f-1bf87edc4491"
stub_terms_type_validated = TermFiles(**stub_terms_file)
stub_device_info = DeviceInfo({"precision": 1}, "")
stub_terms_model = TermsModel(
    unique_id=stub_unique_id,
    terms_type_validated=stub_terms_type_validated,
    terms_version=[1, 5, 3],
    device_info=stub_device_info,
)
