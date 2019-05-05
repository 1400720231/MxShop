



# drf 视图关系入门总结

**View**

```python
from django.views.generic.base import View
class IndexView(View):
    def get(self, request):
        pass
    def post(self, request):
        pass

```

总结：

​	这是django层面得最基本得cbv方式得视图编写方式。对应得类方法get,post分别对应get，post请求。

在路由中可这样使用：url(r'xxx/', IndexView.as_view()))

------

**APIView**

```python
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
```

总结：

​      View源码如下：

```python
class APIView(View):

    # The following policies may be set at either globally, or per-view.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    parser_classes = api_settings.DEFAULT_PARSER_CLASSES
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    throttle_classes = api_settings.DEFAULT_THROTTLE_CLASSES
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
    content_negotiation_class = api_settings.DEFAULT_CONTENT_NEGOTIATION_CLASS
    metadata_class = api_settings.DEFAULT_METADATA_CLASS
    versioning_class = api_settings.DEFAULT_VERSIONING_CLASS

    # Allow dependency injection of other settings to make testing easier.
    settings = api_settings

    schema = DefaultSchema()

    @classmethod
    def as_view(cls, **initkwargs):
        # 省略剩下部分
```

​	很明显APIView继承于View，并在此基础上增加了一些其他属性，如permission_classes权限属性等。需要注意得是此时还没有封装serializer_class属性。在路由中可这样使用：url(r'xxx/', ListUsers.as_view()))

------

**Generic view**

```python
from django.contrib.auth.models import User
from myapp.serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

# 视图函数实现功能方式一
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
```

GenericView源码如下：

```python
class GenericAPIView(views.APIView):
    """
    Base class for all other generic views.
    """
    # You'll need to either set these attributes,
    # or override `get_queryset()`/`get_serializer_class()`.
    # If you are overriding a view method, it is important that you call
    # `get_queryset()` instead of accessing the `queryset` property directly,
    # as `queryset` will get evaluated only once, and those results are cached
    # for all subsequent requests.
    queryset = None
    serializer_class = None

    # If you want to use object lookups other than pk, set 'lookup_field'.
    # For more complex lookup requirements override `get_object()`.
    lookup_field = 'pk'
    lookup_url_kwarg = None

    # The filter backend classes to use for queryset filtering
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS

    # The style to use for queryset pagination.
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get_queryset(self):
        # 省略剩下部分代码
```

GenericAPIView继承了views.APIView，并且在此基础上增加了queryset，serializer_class等属性用来序列化数学据。在路由中可这样使用：url(r'xxx/', UserList.as_view({"get":"list"})))。还有一种方式视图函数可以这么写：

```python
from django.contrib.auth.models import User
from myapp.serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

# 视图函数实现功能方式二
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

    """
理由：
    from rest_framework import mixins
    from rest_framework import generics
    相关源代码：
    class mixins.ListModelMixin(object)
        def list(self, request, *args, **kwargs):
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
           
    class generics.ListCreateAPIView(mixins.ListModelMixin,GenericAPIView)：
        def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)

        def post(self, request, *args, **kwargs):
            return self.create(request, *args, **kwargs)
            
	generics.ListCreateAPIView已经写了get,post方法，并在函数体中调用了self.list(即mixins.ListModelMixin中得list方法)，所以可以像上面得第二种方式，不用重写def list(self,reuqets)
方法，这样在路由中也不用UserList.as_view({"get":"list"})这样绑定了，直接UserList.as_view()即可
    
   """
   
```

------

ViewSet

```python
# https://www.django-rest-framework.org/api-guide/viewsets/
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from myapps.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response

class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
# 路由中大概是这样：
user_list = UserViewSet.as_view({'get': 'list'})
user_detail = UserViewSet.as_view({'get': 'retrieve'})
"""
理由：
from rest_framework import viewsets下面有：
(1)
class ViewSet(ViewSetMixin, views.APIView):
     pass # 这就是该类得全部代码，没有省略
(2)
class ViewSetMixin(object):
    """
    This is the magic.

    Overrides `.as_view()` so that it takes an `actions` keyword that performs
    the binding of HTTP methods to actions on the Resource.

    For example, to create a concrete view binding the 'GET' and 'POST' methods
    to the 'list' and 'create' actions...

    view = MyViewSet.as_view({'get': 'list', 'post': 'create'})
    """

    @classonlymethod
    def as_view(cls, actions=None, **initkwargs):
        cls.suffix = None
        cls.detail = None
        cls.basename = None
        # 生路部分代码
 ViewSetMixin就是重写了as_view()方法，加入了一些属性，变量。比如：action，baseanme等。
 这些action,basename在某些地方是有用得，比如可以根据请求方式来适应路由权限：
 def get_permissions(self):
    # 如果是get就是登陆验证，否则其他请求就需要超级用户才行
    if self.action == 'list':
        permission_classes = [IsAuthenticated]
    else:
        permission_classes = [IsAdmin]
    return [permission() for permission in permission_classes]

"""


```

------

**router**

```python
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
urlpatterns = router.urls

# 作用就是把viewset和url请求方法映射，而不用as_view({"get":"post"})
```

------

```python
总结：

"""
（1）APIView继承于View，增加了permission_classes 等功能
（2）generics.Genericview继承于APIView，增加了serializer_class等功能
（3）viewsets.ViewSet 继承于ViewSetMixin, views.APIView
（4）ViewSetMixin重写了as_view()方法，加入了basename,action等属性为router结合做准备，但是到这里会发现
	views.APIView是没有serializer_class功能得，所以只能手动序列化，不能指明serializer_class属性。所以还衍生了其他得各种排列组合得继承：
		class GenericViewSet(ViewSetMixin, generics.GenericAPIView):
			pass
 (5)一般viewsets下的类和router联用，因为第（4）中表面了里面得类重写了as_view()方式;或者直接单独使用generics中得类，在路由只直接as_view()就行，不用依赖router.
"""


```



