"""iconviewer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter
from api.views import IconViewSet
from api.views import TagViewSet
from api.views import IconSetViewSet
from api.views import GroupViewSet
from api.views import TreeViewSet


UUID_RE = '[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'

router = DefaultRouter()
router.register(r'icons', IconViewSet, basename='icon')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'tree', TreeViewSet, basename='tree')
router.register(r'iconsets', IconSetViewSet, basename='iconset')


schema_view = get_schema_view(title="Icon Viewer API")

urlpatterns = [
    url('^schema$', schema_view),
    url(r'^auth/', include('rest_framework.urls')),
] + router.urls