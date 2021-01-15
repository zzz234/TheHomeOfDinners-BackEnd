from random import randint
import parameters
from rest_framework.response import Response
from rest_framework.views import APIView
from ronglian_sms_sdk import SmsSDK
import time

accId = '8a216da875e463e00175e9f089dd01bf'
accToken = '15e2f16659e045f7becc0aee8e4e99cd'
appId = '8a216da875e463e00175e9f945ac01d9'


def send_message(phone, data):
    """
    发送验证码
    :param phone: 手机号
    :param data: 验证码
    :return: 接口调用结果
    """

    sdk = SmsSDK(accId, accToken, appId)
    # tid = '容联云通讯平台创建的模板'
    tid = '1'
    mobile = phone
    datas = (data, 5)
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)


# Create your views here.
class SMSCodeView(APIView):
    """短信验证码"""

    def get(self, request, mobile):
        # 1.生成验证码
        sms_code = '%06d' % randint(0, 999999)
        # 2.利用容联云通讯发送短信验证码
        send_message(mobile, sms_code)
        parameters.mobile = mobile
        parameters.sms_code = sms_code
        parameters.w_time = time.time()
        # 3.响应
        return Response({'message': 'ok', })
