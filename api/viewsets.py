import uuid
from django.http import FileResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django.shortcuts import get_object_or_404
from api.serializers import IconSerializer
from api.serializers import IconDetailSerializer
from api.serializers import IconSetSerializer
from api.serializers import IconSetDetailSerializer
from api.serializers import TagSerializer
from api.serializers import TagDetailSerializer
from api.serializers import GroupSerializer
from api.serializers import TreeSerializer
from iconviewer.models.tag import Tag
from iconviewer.models.group import Group
from iconviewer.models.iconset import IconSet
from iconviewer.models.icon import Icon



class ResultsSetPagination(PageNumberPagination):
    """Paginate result set"""
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class IconViewSet(viewsets.ReadOnlyModelViewSet):
    """Get an Icon list."""
    queryset = Icon.objects.all()
    serializer_class = IconSerializer
    permission_classes=[IsAuthenticated]
    pagination_class = ResultsSetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'tags__name', 'icon_set__name', 'icon_set__group__name')

    def retrieve(self, request, pk=None):
        """Get icon file details."""
        tag = get_object_or_404(self.queryset, pk=pk)
        serializer = IconDetailSerializer(tag, context={'request': request})
        return Response(serializer.data)

    @action(detail=True)
    def download_icon_file(self, request, **kwargs):
        """Download icon file by UUID."""
        return FileResponse(
            Icon.objects.get(pk=kwargs.get('pk')).file,
            as_attachment=True
        )

    def get_uuid_params(self, *params):
        ret_params = {}
        for param in params:
            value = self.request.query_params.get(param)
            if value:
                ret_params[param] = uuid.UUID(hex=value)
        return ret_params

    def get_queryset(self):
        params = self.get_uuid_params('group', 'iconset', 'node')
        queryset = Icon.objects.all()

        if 'node' in params:
            queryset = queryset.filter(
                icon_set__group__uuid__exact=params['node'].urn
            ) | queryset.filter(
                icon_set__uuid__exact=params['node'].urn
            )
        elif 'group' in params or 'node' in params:
            queryset = queryset.filter(
                icon_set__group__uuid__exact=params['group'].urn
            )
        elif 'iconset' in params:
            queryset = queryset.filter(
                icon_set__uuid__exact   =params['iconset'].urn
            )

        return queryset

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Get a list of tags."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes=[IsAuthenticated]
    pagination_class = ResultsSetPagination

    def retrieve(self, request, pk=None):
        tag = get_object_or_404(self.queryset, pk=pk)
        serializer = TagDetailSerializer(tag, context={'request': request})
        return Response(serializer.data)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Get a list of groups."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes=[IsAuthenticated]
    pagination_class = ResultsSetPagination


class TreeViewSet(GroupViewSet):
    """Get a hierarchical list of groups and sets."""
    queryset = Group.objects.filter(group__isnull=True)
    serializer_class = TreeSerializer
    permission_classes=[IsAuthenticated]
    pagination_class = ResultsSetPagination


class IconSetViewSet(viewsets.ReadOnlyModelViewSet):
    """Get a list of icon sets."""

    queryset = IconSet.objects.all()
    serializer_class = IconSetSerializer
    permission_classes=[IsAuthenticated]
    pagination_class = ResultsSetPagination

    def retrieve(self, request, pk=None):
        tag = get_object_or_404(self.queryset, pk=pk)
        serializer = IconSetDetailSerializer(tag, context={'request': request})
        return Response(serializer.data)