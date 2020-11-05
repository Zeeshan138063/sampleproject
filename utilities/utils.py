"""project level utilities"""
import random
from enum import Enum, unique


@unique
class ExceptionCodes(Enum):
    """exception codes"""

    UNIQUE_VIOLATION = "23505"  # postgresDb error code


def generate_code():
    """generate random code"""
    return "".join(random.choice("0123456789") for i in range(6))


def is_exception_exists(exception, exception_code):
    """
    check the given exception code belongs to given exception
    @param exception: except obj
    @param exception_code: code to check
    @return: True/False
    """

    return (
        hasattr(exception.__cause__, "pgcode")
        and exception.__cause__.pgcode == exception_code
    )
