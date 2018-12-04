"""Store the data meta data attributes of an icon."""
import os
import uuid
from django.db import models


class Tag(models.Model):
    """Store the data meta data attributes of an icon."""

    name = models.CharField(
        max_length=200,
        unique=True,
        db_index=True
    )

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)