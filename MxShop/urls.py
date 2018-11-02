"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
# 导入xadmin把admin全部用admin代替即可,其他不变
import xadmin
from MxShop.settings import MEDIA_ROOT
from django.views.static import serve
from goods.view_base import  GoodList

# 文档函数
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from goods.views import GoodstViewSet, CategoryViewset
from users.views import SmsCodeViewset,UserViewset
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

router = DefaultRouter()
# goods_list = GoodstListView.as_view({
#     'get': 'list',
#
# })
# base_name 路由名称的前缀
router.register(r'goods', GoodstViewSet, base_name='goods')
router.register(r'categorys', CategoryViewset, base_name='categorys')
router.register(r'codes', SmsCodeViewset, base_name='codes')
router.register(r'users', UserViewset, base_name='users')

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    # medai访问服务配置
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 商品列表页（原生django cbv完成的）
    # url(r'goods/$', GoodList.as_view(), name='goods-list'),

    # -------下面是drf相关路由---------

    # viewser+router方式配置路由
    url(r'', include(router.urls)),

    # drf登陆路由|在drf的browser页面登陆有效
    url(r'^api-auth/', include('rest_framework.urls')),

    # auth_token路由配置
    # url(r'^api-token-auth/', views.obtain_auth_token),


    # jwt的认证接口,返回jwt token值
    url(r'^login/', obtain_jwt_token),

    # drf 路由，views.py中的方式一 、二、三都可以用这个路由
    # url(r'goods/$', GoodstListView.as_view(), name='goods-list'),

    # viewset方式对应的路由形式
    # url(r'goods/$', goods_list, name='goods-list'),
    # drf文档路由
    url(r'docs/', include_docs_urls(title="小熊drf文档界面"))
]
