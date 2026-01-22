"""Application configuration and environment validation."""
import os
import logging

logger = logging.getLogger(__name__)


def validate_env() -> None:
    """Validate required environment variables at application startup."""
    required_vars = (
        "JWT_SECRET_KEY",
        "DATABASE_URL",
    )

    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        logger.error(
            "Missing required environment variables: %s",
            ", ".join(missing),
        )
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}"
        )
