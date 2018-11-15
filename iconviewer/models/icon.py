"""Store the data meta data attributes of an icon."""
import os
import uuid
from django.db import models
from .set import Set
from .tag import Tag


class Icon(models.Model):
    """Store the data meta data attributes of an icon."""

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    parent = models.ForeignKey(
        Set,
        on_delete=models.CASCADE,
        null=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="icons",
        related_query_name="icon"
    )
    file = models.CharField(
        max_length=200
    )
    name = models.CharField(
        max_length=200,
        db_index=True
    )
    svg = models.TextField(
        default=""
    )

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)

    def get_tags(self):
        """
        Return all tags as an array.

        Helper for REST API.
        """
        return [t.name for t in self.tags.all()]
