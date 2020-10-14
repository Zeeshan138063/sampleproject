from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task(name="sum_of_two_numbers")
def add(x, y):
    print(f"{x} + { y}= ")
    return x + y
