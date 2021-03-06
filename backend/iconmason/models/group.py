"""
Store the data meta data attributes of a group.

Groups can have a parent which is can only be a set.
"""
import os
import uuid
from django.db import models


class Group(models.Model):
    """Store the data meta data attributes of a group."""

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    group = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        related_name="groups"
    )
    name = models.CharField(
        max_length=200,
        db_index=True
    )

    sort = models.IntegerField(
        blank=True,
        null=True
    )

    def decendents(self):
        decendents = []
        for child in self.groups.all():
            decendents += [child] + child.decendents()
        return decendents

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)
