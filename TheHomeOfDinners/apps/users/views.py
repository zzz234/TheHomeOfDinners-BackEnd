import re

from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import CreateUserSerializer, UserDetailSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.viewsets import ModelViewSet


class UserView(CreateAPIView):
    """用户注册"""
    # 指定序列化器
    serializer_class = CreateUserSerializer


class UsernameCountView(APIView):

    def get(self, request):
        """
        判断用户是否已存在
        127.0.0.1:8000/username/count?username=yxb
        """
        username = request.GET['username']
        if not re.match(r'\w{5,20}$', username):
            return Response({'message': '用户名格式错误'})
        # 查询user表
        count = User.objects.filter(username=username).count()

        # 包装响应数据
        data = {
            'username': username,
            'count': count,
        }

        # 响应
        return Response(data)


class MobileCountView(APIView):

    def get(self, request):
        """
        判断手机号是否已存在
        127.0.0.1:8000/mobile/count?mobile=12345678910
        """
        mobile = request.GET['mobile']
        if not re.match(r'1[3-9]\d{9}', mobile):
            return Response({'message': '用户名格式错误'})
        # 查询数据库
        count = User.objects.filter(mobile=mobile).count()

        # 包装响应数据
        data = {
            'mobile': mobile,
            'count': count,
        }

        # 响应
        return Response(data)


class UserDetailView(RetrieveAPIView):
    """用户详细信息操作视图"""
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]  # 指定权限，只有通过认证的用户才能访问当前视图

    # def get_object(self):
    #     # 返回当前user对象
    #     return self.request.user  # 因为已经确定了用户通过权限认证，所以此处的user不是匿名对象，有真实数据

    def put(self, request):
        # 修改user属性
        user = self.request.user
        if 'username' in request.data:
            user.username = request.data['username']
        if 'password' in request.data:
            password = request.data['password']
            user.set_password(password)
        user.save()
        return Response(self.get_serializer(user).data)

    def delete(self, request):
        # 删除user
        if 'password' not in request.data:
            return Response({'message': 'need password!'})
        password = request.data['password']
        user = self.request.user
        if user.check_password(password):
            user.delete()
            return Response({'message': 'delete successful!'})
        else:
            return Response({'message': 'password error!'})
