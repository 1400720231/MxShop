from django.shortcuts import render

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
User =get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户登录函数，可以username 或者 mobile
    记得再settings.py下配置:
        AUTHENTICATION_BACKENDS = (
            'users.views.CustomBackend',
        )
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user=User.object.get(Q(username=username)|Q(mobile=username))
            if user.check_pasasword(password):
                return user
        except Exception as e:
            return  None
