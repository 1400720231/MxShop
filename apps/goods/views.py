from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Goods, GoodsCategory
from goods.serializer import GoodsSerializer, CategorySerializer
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
# drf 过滤
from django_filters.rest_framework import DjangoFilterBackend

"""
最底层的drf APIView,继承与django的View(from django.views.generic.base import View)
和直接继承View大体差不多，需要重写get post方法。
APIView 主要在 View增加了一些相关配置，在源码中可以看到如下配置选项：
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    parser_classes = api_settings.DEFAULT_PARSER_CLASSES
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    throttle_classes = api_settings.DEFAULT_THROTTLE_CLASSES
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
    content_negotiation_class = api_settings.DEFAULT_CONTENT_NEGOTIATION_CLASS
    metadata_class = api_settings.DEFAULT_METADATA_CLASS
    versi


class GoodstListView(APIView):
   
    这里是对GoodstListView的解释信息，在浏览器可以看到这条信息
    
    # 获取数据
    def get(self, request, format=None):
        goods = Goods.objects.all()
        serializer = GoodsSerializer(goods, many=True)
        return Response(serializer.data)

    # 保存数据
    def post(self, request, format=None):
        # 和django不同的是data信息直接在request.data里面，因为drf在django
        # 的request进行了一层封装，不是原生django的request
        serializer = GoodsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
"""

"""
方式二：mixins.ListModelMixin + GenericAPIView
GenericAPIView: 
        继承与APIView, 内置了queryset和serializer_class属性，
        queryset 意义就是要序列化的QuerySet对象
        serializer_class 的意义就是知名序列化器，意义就是用serializer_class
        的序列化器去序列化queryset中指定的QuerySet对象们

mixins.ListModelMixin:
        提供GET方法的功能返回serializer.data，实现了方式一中的get功能
        


class GoodstListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Goods.objects.all()[:10]
    serializer_class = GoodsSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)


"""

"""
方式三：generics.ListAPIView并且实现自定义分页功能

generics.ListAPIView(mixins.ListModelMixin, generics.GenericAPIView))
源码中就是继承了ListModelMixin和GenericAPIView，这是可以理解的，因为你能想到把
这些用的多的功能组合，drf肯定也能组合好直接给你用。

自定义分页class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10 # 每页默认数据个数
    page_size_query_param = "page_size"  # 自定义获取每页数据数量的参数，最大不会超过max_page_size=100
    page_query_param = "p" # 第几页
    max_page_size = 100  # 每页最大回去个数


class GoodstListView(generics.ListAPIView):
    
    这里是对GoodstListView的解释信息，在浏览器可以看到这条信息
    
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = StandardResultsSetPagination
"""

"""
方式4： viewsets + router
viewsets.GenericView:
    主要作用是重写了as_view()方法，主要是可以完成方法之间的绑定。
    比如这里的方式4是viewsets.GenericView+mixins.ListModelMixin，
    由方式二可知我们需要重载get方法来实现数据展示的功能，as_view()被重写
    之后可以另外实现在urls.py中如下：
    from goods.views import GoodsListViewSet
    goods_list = GoodsListViewSet.as_view(
            {
            'get':list,
            }
            )
    urlpatterns = [
        url(r'goods/$', goods_list, name='xxx'),
    ]
    
    ------------
    所以'get':'list'的意义就是完成了方式二中的重载get方式，也就是实现的下面这几行代码（注意get和self.list）：
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
        
但是这样写{'get':'list'}还是有点麻烦，drf有没有也顺便帮忙稍微封装一下呢？router的作用就是在此
urls.py中如下：
from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from goods.views import GoodstListView


router = DefaultRouter()
router.register(r'goods', GoodstListView) # 注册goods路由,会自动实现上面的'get':'list'的功能  
 urlpatterns = [
        url(r'', include(router.urls)),
     
    ]


"""


# 自定义分页class


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12  # 每页默认数据个数
    page_size_query_param = "page_size"  # 自定义获取每页数据数量的参数，最大不会超过max_page_size=100
    page_query_param = "page"  # 第几页
    max_page_size = 100  # 每页最大回去个数


"""
# 过滤方式一 重载get_queryset方法，和django中是一样的用法
class GoodstListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    # queryset = Goods.objects.all() # get_queryse重载后这个就没有用了
    serializer_class = GoodsSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        return Goods.objects.filter(shop_price__gt=100)
"""

# 过滤方式二：drf filter
"""
pip install django_filters
在settings.py中installed_apps中配置
方式一：
from django_filters.rest_framework import DjangoFilterBackend
class GoodstListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all() # get_queryse重载后这个就没有用了
    serializer_class = GoodsSerializer # 序列化器
    pagination_class = StandardResultsSetPagination  # 分页器
    # 这里的元组一定要加逗号！！！！不然后报错！！！
    filter_backends = (DjangoFilterBackend, ) # 过滤器，是django的过滤器，
    filter_fields = ('name', 'shop_price')  # 指定过滤字段
缺点：
    filter_fields中的字段只能精确匹配，要想模糊查询，可以按照方式二中的办法自定义filter_class
    

方式二：
要像模糊匹配可以自定义一个filter类，django_filter官网：https://django-filter.readthedocs.io/en/master/
filters.py下：

import django_filters
from .models import Goods
class ProductFilter(django_filters.rest_framework.FilterSet):
    # 自定义一个字段，过滤model中的shop_price字段， 方式为大于等于(gte)
    price_min = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte')
    # 自定义一个字段，过滤model中的shop_price字段， 方式为大于等于(lte)
    price_max = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte')
    # 自定义一个字段，过滤model中的category__name(category的外键实例的name字段， 方式为不区分大小写模糊查询（icontains）
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    # 定义一个字段，过滤model中的name, 方式为不区分大小写模糊查询（icontains）
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'name', 'category_name']

views.py下：

from  .filters import ProductFilter

注释掉filter_fields = ('name', 'shop_price')这一行，因为在filter_class中定义了
用来搜索的fields=['name',......]
class GoodstListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all() # get_queryse重载后这个就没有用了
    serializer_class = GoodsSerializer # 序列化器
    pagination_class = StandardResultsSetPagination  # 分页器
    # 这里的元组一定要加逗号！！！！不然后报错！！！
    filter_backends = (DjangoFilterBackend, ) # 过滤器，DjangoFilterBackend是django的过滤器，
    filter_class = ProductFilter
   
    

方式三：
上面的DjangoFilterBackend就是django中的过滤方式，drf中也有一个方式可以过滤，SearchFilter。
SearchFilter是用来做模糊查询的最佳效果

from .filters import ProductFilter
from rest_framework.filters import SearchFilter
class GoodstListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all() # get_queryse重载后这个就没有用了
    serializer_class = GoodsSerializer # 序列化器
    pagination_class = StandardResultsSetPagination  # 分页器
    # 这里的元组一定要加逗号！！！！不然后报错！！！
    filter_backends = (DjangoFilterBackend, ProductFilter) # 过滤器，DjangoFilterBackend是django的过滤器，
    filter_class = ProductFilter
    search_fields =('=name','^goods_desc', 'goods_brief')
    # =name表示对name字段精确匹配| ^goods_desc表示对goods_desc以搜索内容开头进行搜索| goods_brief就是模糊搜索
"""

from .filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter


class GoodstViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    DjangoFilterBackend  过滤功能
    SearchFilter  搜索功能
    OrderingFilter  排序功能
    """
    queryset = Goods.objects.all()  # get_queryse重载后这个就没有用了
    serializer_class = GoodsSerializer  # 序列化器
    pagination_class = StandardResultsSetPagination  # 分页器
    # 这里的元组一定要加逗号！！！！不然后报错！！！
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)  # 过滤器，是django的过滤器，
    filter_class = ProductFilter
    # SearchFilter指定搜索字段=name表示精确匹配，^goods_desc表示以搜索字段开头的内容（正则）
    search_fields = ('name', '^goods_desc', 'goods_brief')
    # OrderingFilter指定排序指端| 根据sold_num和add_time,shop_price排序
    # 也可以指定非时间或者数字字段排序，比如这里的name，但是好像从排序结果来看没有什么意义。。。
    ordering_fields = ('sold_num', 'add_time', 'shop_price', 'name')
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)


class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据,类目数据很少就不用分页，只序列化就行了

    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
