from django.conf.urls import include, url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    url(r'^musicplayer/', include(('musicplayer.urls', 'musicplayer'))),
]

