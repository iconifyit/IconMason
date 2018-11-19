"""Store the data meta data attributes of an icon."""
import os
from iconviewer.settings import MEDIA_ROOT
import uuid
from django.db import models
from django.core.files.storage import FileSystemStorage
from iconviewer.models.iconset import IconSet
from iconviewer.models.tag import Tag


class Icon(models.Model):
    """Store the data meta data attributes of an icon."""

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    icon_set = models.ForeignKey(
        IconSet,
        on_delete=models.CASCADE,
        null=True,
        related_name="icons",
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="icons",
        related_query_name="icon"
    )
    name = models.CharField(
        max_length=200,
        db_index=True
    )

    file = models.ImageField(
        storage=FileSystemStorage(location=MEDIA_ROOT),
        upload_to='svg',
        default="",
        max_length=200
    )

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)