from rest_framework import serializers
from .models import ShoppingCart
from goods.models import Goods
from .models import OrderInfo
from goods.serializer import GoodsSerializer

class ShoppingCartSerializer(serializers.Serializer):
    # 获取当前登陆的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1,
                                    error_messages={
                                        "min_value": "商品数量不不能小于1",
                                        "required": "请选择购买数量"
                                    })
    goods =serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    """
    serializers --> views--->数据库
    当为serializers.Serializer的时候必须重载create实现save
    当为serializers.ModelSerializer的时候内部重载了create
    也就是说再serializers层面已经save到数据库了，但是调用再views层面！
    理由：
        mixin中调用的serializer.save()实际上就是serializers中的save方法,save()方法会调用自己的create()方法，
    然而当为serializers.ModelSerializer的时候，内部做了create()方法重载，并保存到数据库，但是serializers.Serializer
    的create()方法源码如下：
        def create(self, validated_data):
         raise NotImplementedError('`create()` must be implemented.')
    仅仅只是把报错告诉你要自己实现create方法。所以我们使用serializers.Serializer这里必须重载
    """

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        # 返回保存数据库后的instance
        return existed

    # 同上需要重载update
    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    # 获取当前登陆的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    def generate_order_sn(self):
        import time
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{user_id}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                        user_id=self.context["request"].user.id,
                                                        ranstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model =OrderInfo
        fields = ("__all__")