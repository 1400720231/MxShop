from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework import mixins
from .serializers import UserFavSerializer
from .models import UserFav
# Create your views here.


class UserFavViewset(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    用户收藏功能

    这个serializer_class要保存当前登陆的用户：
        user =serializers.HiddenField(
            default=serializers.CurrentUserDefault()
        )
    这个字段是要求登陆的，不然会报错匿名用户。。所以必须指定permission_classes参数，
    而且你会发现其实你再系统中是登陆的状态，但是再站点中post数据的时候还是会报错，仅仅是因为没有指定
    permission_classes参数。。。。也就是说就算登陆了不指定permission_classes参数再此
    视图中也算作没登陆。。
    get_queryset:
        重载该方法是为了返回当前用户的数据
    IsOwnerOrReadOnly：
        该自定义权限是为了限制在编辑或者删除的时候，只能操作自己用户下的数据，
        在此视图中主要是体现删除操作的时候只能删除自己用户收藏的。删除不是自己的
        数据的时候会报404 not found
    ps:
        其实get_queryset返回的就是当前用户的数据，按道理拿着这些数据去删除是
    不会报错的，但是为了保证绝对的可靠性，要是某个人(爬虫)拿到这个删除api去删除不属于自那个
    的数据那就gg了，所以IsOwnerOrReadOnly是完全有必要的
    """
    # queryset = UserFav.objects.all()
    serializer_class =UserFavSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        queryset = UserFav.objects.filter(user=self.request.user)
        return  queryset
