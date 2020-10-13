import random


def generate_code():
    return "".join(random.choice("0123456789") for i in range(6))
