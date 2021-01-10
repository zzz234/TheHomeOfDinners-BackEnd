from django.conf.urls import url, include
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views
from rest_framework.routers import SimpleRouter

urlpatterns = [
    # 注册用户
    url(r'^users/$', views.UserView.as_view()),
    # 判断用户名是否已注册
    url(r'^username/count$', views.UsernameCountView.as_view()),  # \w表示字母数字下划线
    # url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),  # \w表示字母数字下划线
    # 判断手机号是否已注册
    url(r'^mobile/count$', views.MobileCountView.as_view()),
    # url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    # JWT登录
    url(r'^login/$', obtain_jwt_token),  # 内部认证代码还是Django中的  登录成功生成token

    # 获取用户详情
    url(r'^user/(?P<pk>[^/.]+)/$', views.UserDetailView.as_view()),

]
