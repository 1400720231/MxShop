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


class UserRegSerializer(serializers.ModelSerializer):
    # code一定要在fields=()声明，不然会报错
    code = serializers.CharField(required=True, max_length=4, min_length=4,
                                 write_only=True,
                                 label="label短信验证码", help_text="help_text短信验证码",
                                 error_messages={
                                    "blank": "请输入验证码", # 字段存在，内容为空
                                    "required": "请输入验证码", # 字段不存在，没有传过来
                                    "max_length": "验证码格错误",
                                    "min_length": "验证码格式错误"
                                })

    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    """
    validators: 检验器
        UniqueValidator：唯一检验
            检验目标： queryset=User.objects.all()，目标要唯一
        message： 当触发UniqueValidator的时候的返回的报错信息
    """
    password = serializers.CharField(style={"input_type": "password"},
                                     label="密码",help_text="密码",
                                     write_only=True)

    def validate_code(self, code):
        """
        知识点：
            1、 self.initial_data
                前端post过来的数据在self.initial_data中

            2、self.context['view'].request.query_parmas
                url后面问号带的参数在其中：www.baidu.com/?a=xx&b=xxx


        """
        verify_codes = VerifyCode.objects.filter(mobile=self.initial_data["mobile"]).order_by("-add_time")
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
        """
            首先，整个逻辑是先根据serializers中的字段验证保存数据库，
        然后再serializers中的字段序列化展示出来。
            因为UserProfile中没有code字段，不删除的话，会将code字段保存数据库，
        但是model中找不到code字段，会报错；而write_only=True参数则是为了防止序列化展示出来的
        时候报错，UserProfile中没有code字段。

        """
        # attrs["username"] = attrs["mobile"]
        del attrs["code"]
        return attrs

    def create(self, validated_data):
        """
        方式一：
            ModelSerializer才有create方法，当password验证通过后会直接存进数据库，
        而且是明文的未加密，所以这里重载create函数为的是调用model的.set_paassword函数，
        当然你也可以不重载create函数，在validate函数里面对password加密，实现set_password
        的功能作用也是一样的。
            源码中有这样一句话：
                try:
                    instance = ModelClass.objects.create(**validated_data)
                except ....
                    .....
                return instance
            意思就是，在create函数中就保存进数据库了。所以这里当user.set_password()之后，
        一定得user.save()不然密码还是明文。
        方式二：
            见signals.py的内容
        :param validated_data:
        :return:
        """
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save() # 一定要save一下
        return user

    class Meta:
        model = User
        fields = ("mobile", "username", "code", "password")


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")