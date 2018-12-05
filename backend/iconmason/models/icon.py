"""Store the data meta data attributes of an icon."""
import uuid
import re
import os
from pathlib import Path
from django.db import models
from django.core.files.storage import FileSystemStorage
from iconmason.models.iconset import IconSet
from iconmason.models.tag import Tag
from iconmason.settings import MEDIA_ROOT
from pygments import highlight
from pygments.lexers import XmlLexer
from pygments.formatters import HtmlFormatter
from defusedxml.minidom import parseString

def upload_path(instance, filename):
    group_path = []
    node = instance.icon_set
    while node:
        group_path.append(node.name)
        node = node.group
    return "icons/{group_path}/{filename}".format(
            group_path = os.pathsep.join(reversed(group_path)),
            filename=filename
        )

IMAGE_TYPE_RASTER = ("jpg", "jpeg", "gif", "png", "bmp", "tiff", "img", "ico")
IMAGE_TYPE_VECTOR = ("svg", "eps", "ai", "pdf", "ps", "stl", "cdr")

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
        upload_to=upload_path,
        default="",
        max_length=200
    )

    @property
    def filetype(self):
        ext = Path(self.file.name).suffix.lower().strip(".")
        if ext == "svg":
            return "SVG"
        if ext in IMAGE_TYPE_VECTOR:
            return "Vector"
        if ext in IMAGE_TYPE_RASTER:
            return "Raster"
        return "Unknown"

    @property
    def filename(self):
        return Path(self.file.name).name

    @property
    def is_svg(self):
        return Path(self.file.name).suffix.lower() == ".svg"

    @property
    def svg_data(self):
        if not self.is_svg:
            return False
        data = self.file.read()
        self.file.close()
        return data

    @property
    def svg_source(self):
        if not self.is_svg:
            return False
        parsed = parseString(self.svg_data)
        pretty = parsed.toprettyxml(indent="  ", newl="\n")
        pretty = "\n".join([l for l in pretty.split("\n") if l.strip()])
        return highlight(pretty, XmlLexer(), HtmlFormatter())

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)
