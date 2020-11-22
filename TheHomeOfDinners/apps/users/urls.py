from django.conf.urls import url, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('user', views.UserDetailView)

urlpatterns = [
    # 注册用户
    url(r'^users/$', views.UserView.as_view()),
    # 判断用户名是否已注册
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),  # \w表示字母数字下划线
    # 判断手机号是否已注册
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
]
urlpatterns += router.urls
