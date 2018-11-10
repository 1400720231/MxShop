from django.shortcuts import render

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
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


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
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
        # 如果能走到这里说明都验证通过了|validated_data包含了验证过的字段信息
        mobile = serializer.validated_data['mobile']

        # 下面似乎短信验证码的发送逻辑,因为没有短信机制，我就随便写个函数
        code_status = self.send()
        # 如果发送成功
        if code_status:
            verify_code = VerifyCode(code=code_status, mobile=mobile)
            verify_code.save()
            return Response({'mobile': mobile}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': '验证码发送失败，请稍后再试'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserViewset(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin ,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """


    """
    queryset = User.objects.all()
    serializer_class = UserRegSerializer
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)

    # 动态序列化 注册和获取为两个序列化
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer

    # 动态权限 注册不需要权限，获取详情需要
    def get_permissions(self):
        if self.action == "retrieve":
            return [IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 注册成功后，去拿jwt_token序列化回去
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        # 拿token
        re_dict["token"] = jwt_encode_handler(payload)
        # 返回用户名
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        # 序列化回去
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)
