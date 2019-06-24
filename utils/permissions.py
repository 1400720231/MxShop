from rest_framework import permissions

# 官网地址： https://www.django-rest-framework.org/api-guide/permissions/#examples


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user

"""
注意这里的
    return obj.user == request.user
model中的字段是user,obj.user才是这样，
要是model中的字段是xxx,那这里就是obj.xxx  == request.user
"""