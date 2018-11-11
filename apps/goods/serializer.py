from rest_framework import serializers
from .models import Goods,GoodsCategoryBrand, GoodsCategory, GoodsImages, Banner
from django.db.models import Q
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


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImages
        fields = ("image",)


# 1 在Goods中category是一个外键，所以我们先序列化category对应的model Category
# 2 在父级serializer中单独指明外键字段的序列化对象
class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        # 可以指定需要序列化的字段
        # fields = ('name','click_num')
        # 或者直接"__all__"序列化所有字段
        fields = '__all__'

    # 获取url后面带的参数方法
    # def validated_data(self):
    #   self.context['view'].request.query_parmas


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
    """
    1、
        序列化的时候是序列化最上层的数据的，所以GoodsCategory只返回最上层的数据，
     sub_cat = CategorySerializer2(many=True)表示返回两层数据

    2、
        def get_goods(self, obj):
            all_goods = Goods.objects.filter(Q(category_id=obj.id)|\
                                             Q(category__parents_category_id=obj.id)\
                                             |Q(category__parents_category__parents_category_id=obj.id))
            goods_serializer = GoodsSerializer(all_goods, many=True)
            return goods_serializer.data

            自定义一个专门返回函数，用来灵活序列化数据。在Goods中有一个字段外键指向GoodsCategory，
        GoodsCategory中有一个字段parents_category，只有第三层数据才有category__parents_category__parents_category_id，
        只有第二层的数据才有category__parents_category_id,当第一层的时候就直接category_id就行，所以
        这个函数的意思就是返回在Goods中为第一类的数据
    3、
        class Meta:
            model =GoodsCategory
        这里的model=GoodsCategory,所以def get_goods(self, obj):中的obj为GoodsCategory的 实例，
        def get_goods(self, obj):方法则是返回所有category对应的商品类是第一类的商品。
    """
    brands = BannerSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2(many=True)

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id)|Q(category__parents_category_id=obj.id)\
                                   |Q(category__parents_category__parents_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True)
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class TempSerialiser(serializers.ModelSerializer):
    # sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = CategorySerializer
        fields = "__all__"