from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('', views.index, name='index'),
    path('<slug:slug>/', views.index, name='index_slug'),
]
