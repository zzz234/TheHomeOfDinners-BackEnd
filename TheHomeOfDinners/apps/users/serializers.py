import re
import time

from rest_framework import serializers

import parameters
from users.models import User
from rest_framework_jwt.settings import api_settings


class CreateUserSerializer(serializers.ModelSerializer):
    """注册序列化器"""

    # 序列化器的所有字段：【'id','username','password','password2','mobile','sms_code','role','allow'】
    # 需要校验的字段：【'username','password','password2','mobile','sms_code','role','allow'】
    # 模型中已存在的字段：【'username','password','mobile'】

    # 需要序列化的字段：【'id','username','mobile'】(需要返回的字段)
    # 需要反序列化的字段：【'username','password','password2','mobile','sms_code','role','allow'】

    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='验证码', write_only=True)
    allow = serializers.CharField(label='同意协议', write_only=True)
    token = serializers.CharField(label='token', read_only=True)

    class Meta:
        model = User  # 从User模型中映射序列化器字段
        fields = ['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'role', 'allow', 'token']
        # read_only_fields = [] #也可以通过read_only_fields指定只读字段
        extra_kwargs = {  # 修改字段选项
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {  # 自定义校验出错后的错误提示信息
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的密码',
                    'max_length': '仅允许5-20个字符的密码',
                }
            },
        }

    def validate_mobile(self, value):
        """单独校验手机号"""
        if not re.match(r'1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式有误')
        return value

    def validate_allow(self, value):
        """是否同意协议校验"""
        if value.lower() != 'true':
            raise serializers.ValidationError('请同意用户协议')
        return value

    def validate(self, attrs):
        """校验密码"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两个密码不一致')

        # # 校验验证码
        # if time.time() - parameters.w_time > 300:
        #     raise serializers.ValidationError('无效的验证码')
        #
        # if attrs['mobile'] != parameters.mobile or attrs['sms_code'] != parameters.sms_code:
        #     raise serializers.ValidationError('验证码错误')

        return attrs

    def create(self, validated_data):
        # 把不需要的字段移除
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']
        # 先取出密码
        password = validated_data.pop('password')
        # 创建用户模型对象
        user = User(**validated_data)
        user.set_password(password)  # 将密码加密
        user.save()  # 存入数据库

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 引用jwt中的jwt_payload_handler函数（生产payload）
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)  # 根据user生成用户相关的载荷
        token = jwt_encode_handler(payload)  # 传入载荷生成jwt

        user.token = token

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情序列化器"""

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'password', 'role']
        extra_kwargs = {  # 修改字段选项
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的密码',
                    'max_length': '仅允许5-20个字符的密码',
                }
            },
        }
