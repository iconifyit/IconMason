from rest_framework.routers import DefaultRouter
from api.viewsets import IconViewSet
from api.viewsets import TagViewSet
from api.viewsets import IconSetViewSet
from api.viewsets import GroupViewSet
from api.viewsets import TreeViewSet

router = DefaultRouter()
router.register(r'icons', IconViewSet, basename='icon')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'tree', TreeViewSet, basename='tree')
router.register(r'iconsets', IconSetViewSet, basename='iconset')