from django.shortcuts import render

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from .serializers import SmsSerializer, UserRegSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import VerifyCode
from random import choice


User =get_user_model()

class CustomBackend(ModelBackend):
    """
    自定义用户登录函数，可以username 或者 mobile
    记得再settings.py下配置:
        AUTHENTICATION_BACKENDS = (
            'users.views.CustomBackend',
        )
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
"""
class CustomBackend(ModelBackend):
   
    
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:

            return None
"""

class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    # 生成一个4位数的随机字符串
    def send(self):
        seeds = '1234567890'
        random_str = []
        for i in range(0, 4):
            random_str.append(choice(seeds))
        return ''.join(random_str)

    # 重载CreateModelMixin中的create方法，完整手机验证码的save()
    def create(self, request, *args, **kwargs):
        # post的数据再request.data中
        serializer = self.get_serializer(data=request.data)
        # 验证失败就报错
        serializer.is_valid(raise_exception=True)
        # 如果能走到这里说明都验证通过了
        mobile = serializer.validated_data['mobile']

        # 下面似乎短信验证码的发送逻辑,因为没有短信机制，我就随便写个函数
        code_status = self.send()
        # 如果发送成功
        if code_status:
            verify_code = VerifyCode(code=code_status, mobile=mobile)
            verify_code.save()
            return Response({'mobile': mobile}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': '验证码发送失败，请稍后再试'}, status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserViewset(CreateModelMixin, viewsets.GenericViewSet):
    """


    """
    serializer_class = UserRegSerializer