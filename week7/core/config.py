"""Application configuration and environment validation."""
import os
from dotenv import load_dotenv

load_dotenv()

def validate_env() -> None:
    """Validate required environment variables at startup."""
    required_vars = [
        "JWT_SECRET_KEY",
        "DATABASE_URL",
    ]

    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}"
        )
