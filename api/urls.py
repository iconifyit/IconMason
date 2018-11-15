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
from .views import ListIconView, RetrieveView
UUID_RE = '[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'

urlpatterns = [
    url(r'^icon/$', ListIconView.as_view(), name="create"),
    url(
        r'^icon/(?P<pk>{})/$'.format(UUID_RE),
        RetrieveView.as_view(),
        name="crud"
    ),
    url(r'^auth/', include('rest_framework.urls'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
