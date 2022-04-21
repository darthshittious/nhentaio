__all__ = (
    "NHentaiError",
    "NotFound",
)


class NHentaiError(Exception):
    """The base exception that all nhentai-related exceptions inherit from."""


class NotFound(NHentaiError):
    """Raised when content is not found, search results are empty, or similar."""
