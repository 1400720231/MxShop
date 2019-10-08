import django_filters
from django.contrib.admin.utils import help_text_for_field

from .models import Goods
from django.db.models import Q


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
        category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
        对Goods model自身的name模糊筛选，其中icontains表示不区分大小写，contains表示区分大小写
        name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    label='最大价格' 表示站点搜索框的抬头字段，不指定该参数的话，抬头显示字段为Goods models中的verbose_name值
    """
    pricemin = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte', help_text="最小值")
    pricemax = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte',  label='最大价格',help_text="最大价格")
    top_category = django_filters.NumberFilter(method='top_category_filter', label='自定义搜索框',help_text='自定义搜索框')
    is_hot = django_filters.BooleanFilter(field_name='is_hot', label="是否热销",help_text='是否热销')

    # 自定义一个搜索方法，传参给method，表示top_category输入的字段用改方法筛选过滤
    def top_category_filter(self, queryset, name, value):
        queryset = queryset.filter(Q(category_id=value)|Q(category__parents_category_id=value)\
                                   |Q(category__parents_category__parents_category_id=value))
        return queryset

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot', 'is_new']