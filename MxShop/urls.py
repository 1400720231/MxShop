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
from trade.views import ShoppingCartViewset
from goods.views import IndexCategoryViewset,GoodstViewSet, CategoryViewset,BannerViewset,pandaviewset,\
    GoodstListView,PandaTestViewt,GoodsCategorySerializerTEST,goodsSerializertestviewst
from users.views import SmsCodeViewset,UserViewset
from trade.views import OrderViewset
from user_operation.views import UserFavViewset,LeavingMessageViewset,AddressViewset
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

router = DefaultRouter()

"""

这种映射的方式只适合GoodstViewSet这种，因为这种视图函数中的ViewSetMixin重写了as_view()方法，提供了可以绑定method:action这种选择
goods_list = GoodstViewSet.as_view({
    'get':'list'
})
"""
# base_name 路由名称的前缀
# 商品
router.register(r'goods', GoodstViewSet, base_name='goods')
# 商品第一大类类别
router.register(r'categorys', CategoryViewset, base_name='categorys')
# 发送短信验证码
router.register(r'codes', SmsCodeViewset, base_name='codes')
# 用户注册
router.register(r'users', UserViewset, base_name='users')
# 用户收藏
router.register(r'userfavs', UserFavViewset, base_name='userfavs')
# 用户留言
router.register(r'messages', LeavingMessageViewset, base_name='messages')
# 收货地址
router.register(r'address', AddressViewset, base_name='address')
# 加入购物车OrderViewset
router.register(r'shoppingcart', ShoppingCartViewset, base_name='shoppingcart')
# 订单相关r
router.register(r'orders', OrderViewset, base_name='orders')
# 轮播图
router.register(r'banners', BannerViewset, base_name='banners')
# 首页商品系列数据
router.register(r'indexgoods',IndexCategoryViewset , base_name='indexgoods')
# 临时验证测测试路由
router.register(r'panda',pandaviewset, base_name='panda')
router.register(r'test',PandaTestViewt, base_name='test')
router.register(r'goodscategorytestViewt',GoodsCategorySerializerTEST, base_name='goodscategorytest')
router.register(r'goodsSerializertestviewst',goodsSerializertestviewst, base_name='goodstest')
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

    # mixin+Generic方式对应的路由
    # url(r'mixin_view_generic/$', GoodstListView.as_view(), name='mixin_view_generic'),

    # View方式对应的路由形式
    # url(r'view_base_goods/$', GoodList.as_view(), name='view_base_goods'),
    # drf文档路由
    url(r'docs/', include_docs_urls(title="小熊drf文档界面"))
]
