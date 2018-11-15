from django.http import HttpResponse
from rest_framework import generics
from .serializers import IconSerializer
from iconviewer.models import Icon, Tag, Group


class ListIconView(generics.ListAPIView):
    """This class defines the create API behaviour for icons."""

    queryset = Icon.objects.all()
    serializer_class = IconSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new Icon."""
        serializer.save()


class RetrieveView(generics.RetrieveAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Icon.objects.all()
    serializer_class = IconSerializer
