import re
from datetime import datetime

from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken, jwt_response_payload_handler

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

    def put(self, request, pk):
        # 修改user属性
        user = User.objects.get(id=pk)
        if 'username' in request.data:
            user.username = request.data['username']
        if 'password' in request.data:
            password = request.data['password']
            user.set_password(password)
        if 'mobile' in request.data:
            user.mobile = request.data['mobile']
        user.save()
        return Response(self.get_serializer(user).data)

    def delete(self, request, pk):
        # 删除user
        if 'password' not in request.data:
            return Response({'message': 'need password!'})
        password = request.data['password']
        user = User.objects.get(id=pk)
        if user.check_password(password):
            user.delete()
            return Response({'message': 'delete successful!'})
        else:
            return Response({'message': 'password error!'})


class UserLoginView(ObtainJSONWebToken):
    # 重写了LoginView来进行错误检测
    def post(self, request, *args, **kwargs):
        # 先把role参数提出来
        role = request.data['role']
        username = request.data['username']
        user_count = User.objects.filter(username=username).filter(role=role).count()
        if user_count != 1:
            return Response("指定角色没有相匹配的用户", status=status.HTTP_510_NOT_EXTENDED)
        data = request.POST
        # 记住旧的方式
        _mutable = data._mutable
        # 设置_mutable为True
        data._mutable = True
        # 改变你想改变的数据
        del request.data['role']
        # data['name'] = 'chenxinming'
        # 恢复_mutable原来的属性
        data._mutable = _mutable
        # -------------------------------------------------

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_509_BANDWIDTH_LIMIT_EXCEEDED)
