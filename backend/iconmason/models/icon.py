"""Store the data meta data attributes of an icon."""
import uuid
import re
from django.db import models
from django.core.files.storage import FileSystemStorage
from backend.models.iconset import IconSet
from backend.models.tag import Tag
from backend.settings import MEDIA_ROOT
from pygments import highlight
from pygments.lexers import XmlLexer
from pygments.formatters import HtmlFormatter
from defusedxml.minidom import parseString


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

    @property
    def svg_data(self):
        return self.file.read()

    @property
    def svg_source(self):
        parsed = parseString(self.svg_data)
        pretty = parsed.toprettyxml(indent="  ", newl="\n")
        pretty = "\n".join([l for l in pretty.split("\n") if l.strip()])
        return highlight(pretty, XmlLexer(), HtmlFormatter())

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)