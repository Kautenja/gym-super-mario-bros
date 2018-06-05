"""Errors for the project."""


class DependencyNotFoundError(OSError):
    """An error signaling that a necessary dependency was not found."""
    pass


__all__ = [
    DependencyNotFoundError.__name__
]
