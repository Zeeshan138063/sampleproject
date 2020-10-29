"""Python user-defined custom exceptions class"""


class MyCustomError(Exception):
    """custom exception class to sent a custom message."""

    def __init__(  # pylint: disable=bad-continuation, missing-docstring, super-init-not-called
        self, *args
    ):
        self.message = None
        if args:
            self.message = args[0]

    def __str__(self):  # pylint: disable=missing-docstring
        return self.message if self.message else "MyCustomError has been raised"
