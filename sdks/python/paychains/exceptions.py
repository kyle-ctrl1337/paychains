"""PayChains SDK exceptions."""


class PayChainsError(Exception):
    """Base exception for all PayChains SDK errors."""

    def __init__(self, message: str, status_code: int | None = None, response: dict | None = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class AuthenticationError(PayChainsError):
    """Raised when the API key is invalid or missing (401)."""


class NotFoundError(PayChainsError):
    """Raised when a requested resource does not exist (404)."""


class RateLimitError(PayChainsError):
    """Raised when the API rate limit has been exceeded (429)."""


class ValidationError(PayChainsError):
    """Raised when the request payload fails validation (422)."""
