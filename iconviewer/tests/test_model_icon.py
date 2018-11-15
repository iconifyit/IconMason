from django.test import TestCase
from iconviewer.models import Icon, Tag, Group


class IconTestCase(TestCase):
    """This class defines the test suite for the Icon model."""

    fixtures = ['iconviewer/tests/fixtures/icon.json']

    def test_model_create(self):
        """Test creating an Icon."""
        i = Icon()
        i.name = "TestIcon"
        i.path = "testicon.svg"
        i.parent = Group.objects.get(pk="59b1c335-bf3c-4fc6-9d17-7c7f91942cfd")

    def test_model_get(self):
        """Test model can find an Icon."""
        i = Icon.objects.get(name__contains="Nice")
        self.assertEquals(i.name, "Nice Icon")

