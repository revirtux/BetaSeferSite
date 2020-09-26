from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('initdb', views.initdb, name='initdb'),
    path('cleardb', views.cleardb, name='cleardb'),
    path('init_houses', views.init_houses, name='init_houses'),
    path('scrap', views.import_old_site, name='scrap'),
    path('<slug:house_name>.css', views.dynamic_css, name='dynamic_css'),
    path('<slug:house_name>', views.house_path, name='house_path')
]