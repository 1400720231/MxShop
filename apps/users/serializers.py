import re
import datetime
from datetime import timedelta
from MxShop.settings import REGEX_MOBILE

from django.contrib.auth import get_user_model
from .models import VerifyCode
from rest_framework import serializers


User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)
    # 方法名字一定以validate开头，后面的mobile和self后面的mobile可以随便取

    def validate_mobile(self, mobile):
        """
        验证手机号码

        :param mobile:
        :return:
        """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证发送频率
        one_minutes_ago = datetime.datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile):
            raise serializers.ValidationError("发送时间频率过快，请再一分钟以后再试。")

        return mobile
