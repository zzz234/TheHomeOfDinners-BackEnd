from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import CreateUserSerializer, UserDetailSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class UserView(CreateAPIView):
    """用户注册"""
    # 指定序列化器
    serializer_class = CreateUserSerializer


class UsernameCountView(APIView):
    """判断用户是否已注册"""

    def get(self, request, username):
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
    """判断用户是否已注册"""

    def get(self, request, mobile):
        # 查询数据库
        count = User.objects.filter(mobile=mobile).count()

        # 包装响应数据
        data = {
            'mobile': mobile,
            'count': count,
        }

        # 响应
        return Response(data)


class UserDetailView(APIView):
    """用户详细信息展示"""

    # serializer_class = UserDetailSerializer

    # queryset = User.objects.all()

    def get(self, request, pk):
        pk = int(pk)
        user = User.objects.get(pk=pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    # permission_classes = [IsAuthenticated]  # 指定权限，只有通过认证的用户才能访问当前视图

    # def get_object(self):
    #     return self.request.user


class UserDetailByMobileView(APIView):
    """用户详细信息展示"""

    # serializer_class = UserDetailSerializer

    # queryset = User.objects.all()

    def get(self, request, mobile):
        try:
            user = User.objects.get(mobile=mobile)
            serializer = UserDetailSerializer(user)
            return Response(serializer.data)
        except:
            return Response({'message': 'No User!'})
    # permission_classes = [IsAuthenticated]  # 指定权限，只有通过认证的用户才能访问当前视图

    # def get_object(self):
    #     return self.request.user
