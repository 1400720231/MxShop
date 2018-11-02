import re
import datetime
from datetime import timedelta
from MxShop.settings import REGEX_MOBILE

from django.contrib.auth import get_user_model
from .models import VerifyCode
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)
    # 方法名字一定以validate开头，后面的mobile和self后面的mobile可以随便取

    def validate_mobile(self, mobile):
        """
        验证手机号码，验证成功后必须把mobile return回去，不然数据库不会保存mobile
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


class UserRegSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, max_length=4, min_length=4, label="label短信验证码", help_text="help_text短信验证码")


    def validate_code(self, code):
        """
        知识点：
            1、 self.initial_data
                前端post过来的数据在self.initial_data中

            2、self.context['view'].request.query_parmas
                url后面问号带的参数在其中：www.baidu.com/?a=xx&b=xxx


        """
        verify_codes = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_codes:
            last_recods = verify_codes[0]
            five_minites_ago = datetime.datetime.now() - timedelta(minutes=5)
            if five_minites_ago > last_recods.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_recods.code != code:
                raise serializers.ValidationError("验证码错误")
            # return code 如果这个code字段是需要保存在数据库中的字段的话，就必须return code回去
        else:
            raise serializers.ValidationError("验证码错误")

    # 所有的serializer字段都在attrs其中
    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("mobile", "username", "email")