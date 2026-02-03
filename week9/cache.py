"""Caching utilities for storing and retrieving LLM responses."""
from typing import Optional
from sqlalchemy.orm import Session
from week7.db.session import engine
from week9.constants import OPENAI_MODEL
from langchain_community.cache import FullLLMCache


def _get_cache_key(question: str) -> str:
    """Deterministic key: normalize question"""
    return question.strip().lower()


def get_cached_answer(question: str) -> Optional[str]:
    """Retrieve cached answer if available from the FullLLMCache table."""
    key = _get_cache_key(question)
    with Session(engine) as session:
        entry = (
            session.query(FullLLMCache)
            .filter_by(prompt=key, llm=OPENAI_MODEL)
            .order_by(FullLLMCache.idx.asc())
            .first()
        )
        return entry.response if entry else None

def store_answer(question: str, answer: str) -> None:
    """Store a new answer in the FullLLMCache table."""
    key = _get_cache_key(question)
    with Session(engine) as session:
        entry = FullLLMCache(prompt=key, llm=OPENAI_MODEL, idx=0, response=answer)
        session.add(entry)
        session.commit()