from rest_framework import serializers
from .models import UserFav
from rest_framework.validators import UniqueTogetherValidator


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