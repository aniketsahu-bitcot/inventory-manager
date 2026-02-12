"""Caching utilities for storing and retrieving LLM responses."""
from typing import Optional
from sqlalchemy.orm import Session
from week7.db.session import engine
from week9.constants import OLLAMA_MODEL
from langchain_community.cache import FullLLMCache


def _get_cache_key(question: str, user_id: int) -> str:
    """Deterministic key: normalize question + user scope"""
    normalized_question = question.strip().lower()
    return f"user:{user_id}:{normalized_question}"



def get_cached_answer(question: str, user_id: int) -> Optional[str]:
    """Retrieve cached answer scoped to the user."""
    key = _get_cache_key(question, user_id)

    with Session(engine) as session:
        entry = (
            session.query(FullLLMCache)
            .filter_by(prompt=key, llm=OLLAMA_MODEL)
            .order_by(FullLLMCache.idx.asc())
            .first()
        )
        return entry.response if entry else None

def store_answer(question: str, answer: str, user_id: int) -> None:
    """Store a new answer scoped to the user."""
    key = _get_cache_key(question, user_id)

    with Session(engine) as session:
        entry = FullLLMCache(prompt=key, llm=OLLAMA_MODEL, idx=0, response=answer)
        session.add(entry)
        session.commit()