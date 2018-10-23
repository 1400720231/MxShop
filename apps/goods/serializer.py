from rest_framework import serializers
from goods.models import Goods, GoodsCategory

"""
drf方式一：serializers.Serializer，类似django的form定义，字段一定要和model中的字段名字一样，类型一样


class GoodsSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=100)
    click_num = serializers.IntegerField(default=0)
    goods_front_image = serializers.ImageField()
    add_time = serializers.DateTimeField()

    # 重载create函数，可以接受数据，save()到数据库
    def create(self, validated_data):
        return  Goods.objects.create(**validated_data)
"""

"""
drf方式二：serializers.ModelSerializer，和django中的ModelForm
        用法是一样的，支持Meta元类显示需要序列化的字段

但是外键字段还是显示的外键字段的id，要想把外键的对象也全部序列化出来，请看
方式三        

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        # 可以指定需要序列化的字段
        # fields = ('name','click_num')
        # 或者直接"__all__"序列化所有字段
        fields = '__all__'
"""


"""
方式三： 把外键字段单独拿出来序列化，然后在上一级的序列化中嵌套使用就行
"""

class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"

"""
这是一个一级序列化器，根据 一对多的概念把所有指向当前实例的其他实例序列化处出来。
相当于django中的反向获取所有对象这样:
class modelA(model.Model):
    name = model.CharField()
    
class modelB(model.Model):
    student = models.ForeignKey(name, relate_name= 'sub_cat')

a = modelA()
a.sub_cat.all()

"""

class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        # 可以指定需要序列化的字段
        # fields = ('name',)
        # 或者直接"__all__"序列化所有字段
        fields = '__all__'



# 1 在Goods中category是一个外键，所以我们先序列化category对应的model Category
# 2 在父级serializer中单独指明外键字段的序列化对象
class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Goods
        # 可以指定需要序列化的字段
        # fields = ('name','click_num')
        # 或者直接"__all__"序列化所有字段
        fields = '__all__'



