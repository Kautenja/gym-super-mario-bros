"""Errors for the project."""


class DependencyNotFoundError(OSError):
    """An error signaling that a necessary dependency was not found."""
    pass


# explicitly define the outward facing API for this module
__all__ = [
    DependencyNotFoundError.__name__
]
