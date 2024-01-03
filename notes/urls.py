from . import views
from rest_framework import routers
from django.urls import re_path as url
from django.conf.urls import include

router = routers.DefaultRouter()
router.register('notes', views.NotesViewSet, basename="views")

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
    url(r'^', include(router.urls)),
]