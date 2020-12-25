from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
urlpatterns = [
    url(r'^restaurant/(?P<pk>\d+)/(?P<partial>\w+)/$',
        views.RestaurantModelViewSet.as_view({'put': 'update'})),
    url(r'^tag_restaurant/(?P<param>\w+)/$',
        views.TagRestaurantDetailView.as_view()),
    url(r'^tags/$', views.TagDetailView.as_view()),
]
router.register('restaurant', views.RestaurantModelViewSet)
router.register('collection', views.CollectionModelViewSet)
urlpatterns += router.urls
print(urlpatterns)
