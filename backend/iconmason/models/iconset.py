"""
Store the data meta data attributes of a set.

Sets can have a parent which can only be a set.
"""
import os
import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from iconmason.models.group import Group


class IconSet(models.Model):
    """Store the meta data attributes of a Set."""

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True,
        related_name="iconsets"
    )
    name = models.CharField(
        max_length=200,
        db_index=True
    )

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)
