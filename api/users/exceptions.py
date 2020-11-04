"""define Python user-defined exceptions"""


# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""


class EmailAlreadyExistsError(Error):
    """Raised when the given email address already exists"""
