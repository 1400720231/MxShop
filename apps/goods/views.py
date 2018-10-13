from django.shortcuts import render

# Create your views here.
from .models import Goods
from goods.serializer import GoodsSerializer
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import  generics
from rest_framework import mixins
from rest_framework import viewsets

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
    page_size = 10 # 每页默认数据个数
    page_size_query_param = "page_size"  # 自定义获取每页数据数量的参数，最大不会超过max_page_size=100
    page_query_param = "p" # 第几页
    max_page_size = 100  # 每页最大回去个数


class GoodstListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = StandardResultsSetPagination