from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework import mixins
from .serializers import AddressSerializer,UserFavSerializer, UserFavDetailSerializer,LeavingMessageSerializer
from .models import UserFav,UserLeavingMessage,UserAddress
# Create your views here.


class UserFavViewset(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    list:
        获取用户收餐列表
    retrive:
        某个收藏商品的详情
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
    # userfav/10/详情id默认肯定是数据库的自增id, lookup_field=goods_id表示用数据库
    # 中的goods_id字段来表示,为了更方便
    lookup_field = "goods_id"

    def get_queryset(self):
        queryset = UserFav.objects.filter(user=self.request.user)
        return queryset

    # 动态序列化 注册和获取为两个序列化
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer

        return UserFavDetailSerializer


class LeavingMessageViewset(mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.CreateModelMixin,
                            viewsets.GenericViewSet):

    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        queryset = UserLeavingMessage.objects.filter(user=self.request.user)
        return queryset


class AddressViewset(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):

    """
    上面的视图增删改查都用到了，其实drf已经内置做了这么一个东西：viewsets.ModelViewSet
    收货地址管理
    list:
        获取收获自地址
    create:
        添加收货地址
    update:
        更新收获地址
    destory:
        删除收货地址
    """
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        queryset = UserAddress.objects.filter(user=self.request.user)
        return queryset
