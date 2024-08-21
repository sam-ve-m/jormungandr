from dataclasses import dataclass

from func.src.domain.enums.bureau.enum import BureauType, BureauStatus


@dataclass
class BureauValidation:
    unique_id: str
    transaction_id: str
    status: BureauStatus
    bureau_response: dict
    event_type: BureauType

    @classmethod
    def from_request(cls, raw_account: dict, **kwargs):
        unique_id = raw_account.get('metadata', {}).get('unique_id')
        return cls(
            unique_id=unique_id,
            bureau_response=raw_account,
            **kwargs
        )
