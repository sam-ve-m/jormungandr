# Jormungandr
from ...validators.term_with_order.validator import TermWithOrder


class TokenModel:
    def __init__(self, term_with_order: TermWithOrder, unique_id: str):
        self.unique_id = unique_id

        self.term_type = term_with_order.term_type
        self.term_with_order = term_with_order.dict()

    def build_harpocrates_jwt_content(self):
        template = dict()
        template.update(self.term_with_order)
        template.update(unique_id=self.unique_id)
        return template

    def build_body_content_to_sign_term(self):
        body_content = dict()
        body_content.update(terms_file=[self.term_type])
        return body_content
