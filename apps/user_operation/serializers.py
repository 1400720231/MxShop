from rest_framework import serializers
from .models import UserFav, UserLeavingMessage,UserAddress
from rest_framework.validators import UniqueTogetherValidator,UniqueValidator
from goods.serializer import GoodsSerializer


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer

    class Meta:
        model = UserFav
        fields = ("goods", "id")


# 用户收藏序列化
class UserFavSerializer(serializers.ModelSerializer):
    """
    validators可以写在某个字段里面（users.serializers.py中UserRegSerializer的username），
    也可以指定多个字段是写在Meta里面,比如下面的

    """
    # 获取当前登陆的用户
    user =serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav

        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=("user", "goods"),
                message="该商品已经收藏了，无需再次收藏"
            )
        ]
        fields = ("user", "goods", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    # 获取当前登陆的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 只返回不post
    add_time = serializers.DateTimeField(read_only=True,format="%Y-%m-%d %H:%M")

    class Meta:
        model = UserLeavingMessage
        fields = ("add_time","user", "message_type", "subject", "message","file","id")


class AddressSerializer(serializers.ModelSerializer):
    # 获取当前登陆的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    signer_name = serializers.CharField(required=True, max_length=10, min_length=2,
                                        label="收货人", help_text="收货人",
                                        error_messages={
                                            "blank": "收货人不能为空", # 字段存在，内容为空
                                            "required": "收货人不能为空", # 字段不存在，没有传过来
                                            "max_length": "收货人姓名最大长度为10",
                                            "min_length": "收货人姓名最小长度为2"
                                     })
    signer_mobile = serializers.CharField(required=True,
                                          label="收货人电话", help_text="收货人电话",
                                          error_messages={
                                              "blank": "收货人电话不能为空",  # 字段存在，内容为空
                                              "required": "收货人电话不能为空",  # 字段不存在，没有传过来
                                              "max_length": "收货人姓名最大长度为10",
                                              "min_length": "收货人姓名最小长度为2"

                                        })

    def validate_signer_mobile(self, signer_mobile):
        from MxShop.settings import REGEX_MOBILE
        import re
        if not re.match(REGEX_MOBILE, str(signer_mobile)):
            raise serializers.ValidationError("手机号码不合法，请输入合法的手机号")
        else:
            # return signer_mobile 如果这个signer_mobile字段是需要保存在数据库中的字段的话，就必须returne回去
            return signer_mobile

    class Meta:
        model = UserAddress
        fields = ("user", "province", "city", "address", "signer_name", "signer_mobile", "id")



