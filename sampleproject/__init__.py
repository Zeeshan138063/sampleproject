"""Start celery every time project start"""
from .celery import app as sampleproject

__all__ = ['sampleproject']
