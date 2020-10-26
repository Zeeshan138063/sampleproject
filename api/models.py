"""Create your models here."""
from django.db import models


class LogsMixin(models.Model):
    """Add the generic fields and relevant methods common to support mostly models"""

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        """meta class for LogsMixin"""

        abstract = True
