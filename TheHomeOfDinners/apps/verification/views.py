from django.shortcuts import render
from rest_framework.views import APIView


# Create your views here.
class SMSCodeView(APIView):
    """短信验证码"""

    def get(self, request, mobile):
        # 1.生成验证码
        # 2.利用容联云通讯发送短信验证码
        # 3.响应
        pass
