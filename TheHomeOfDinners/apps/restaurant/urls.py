from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
urlpatterns = [
    url(r'^tag_restaurant/(?P<param>\w+)/$',
        views.TagRestaurantDetailView.as_view()),
    url(r'^tags/$', views.TagDetailView.as_view()),
]
router.register('restaurant', views.RestaurantModelViewSet)
router.register('collection', views.CollectionModelViewSet)
router.register('menu', views.MenuModelViewSet)
router.register('review', views.ReviewModelViewSet)
urlpatterns += router.urls
