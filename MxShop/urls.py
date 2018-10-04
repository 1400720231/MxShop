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
from django.conf.urls import url,include
# from django.contrib import admin
# 导入xadmin把admin全部用admin代替即可,其他不变
import xadmin
from MxShop.settings import MEDIA_ROOT
from django.views.static import serve
from goods.view_base import  GoodList
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^ueditor/', include('DjangoUeditor.urls' )),
    # medai访问服务配置
    url(r'^media/(?P<path>.*)$', serve, {'document_root':MEDIA_ROOT}),

    # 商品列表页
    url(r'goods/$',GoodList.as_view(), name='goods')
]
