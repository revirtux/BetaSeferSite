from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('initdb', views.initdb, name='initdb'),
    path('cleardb', views.cleardb, name='cleardb'),
    path('init_houses', views.init_houses, name='init_houses'),
    path('scrap', views.scrap, name='scrap')
]