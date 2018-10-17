import django_filters

from .models import Goods


class ProductFilter(django_filters.rest_framework.FilterSet):
    """
    自定义商品过滤器
    gte: greater than equl 大于等于
    lte： less than equl 小于等于
    this is a good time to study
    视频中的name='shop_price'已经修改为field_name='shop_price'了！！

    这个过滤器表示：
        筛选出大于等于 price_min小于等于price_max的Goods
        对外键category的属性的name模糊筛选， 其中icontains表示不区分大小写，contains表示区分大小写
        对Goods model自身的name模糊筛选，其中icontains表示不区分大小写，contains表示区分大小写
    """
    price_min = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte')
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'name', 'category_name']