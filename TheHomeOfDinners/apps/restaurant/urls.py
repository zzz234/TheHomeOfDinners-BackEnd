from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter, SimpleRouter

urlpatterns = [
    url(r'^restaurants/$', views.RestaurantView.as_view()),
    url(r'^restaurant/$', views.RestaurantModelViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^restaurant/(?P<pk>\d+)/$',
        views.RestaurantModelViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    url(r'^restaurant/(?P<pk>\d+)/(?P<partial>\w+)/$',
        views.RestaurantModelViewSet.as_view({'put': 'update'})),
]
