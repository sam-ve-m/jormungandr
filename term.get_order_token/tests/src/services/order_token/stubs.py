from func.src.domain.validators.term_with_order.validator import TermWithOrder

payload = {
    "order": {
        "symbol": "PETR4",
        "quantity": 5,
        "quote_type": "stock"
    },
    "term_type": "term_refusal"
}
term_with_order = TermWithOrder(**payload)

stub_unique_id = "40db7fee-6d60-4d73-824f-1bf87edc4491"