from src.domain.models.request.model import TermModel
from src.repositories.cache.repository import CacheRepository
from src.repositories.terms.repository import (
    TermRepository,
)


class TermService:
    @staticmethod
    async def get_term_url(term: TermModel) -> str:
        term_type = term.file_type
        cached_term = CacheRepository.get_cached_term(term_type.value)
        if cached_term:
            return cached_term
        link = await TermRepository.get_term_link(term_type)
        CacheRepository.save_term_in_cache(term_link=link, term_file=term_type.value)
        return link
