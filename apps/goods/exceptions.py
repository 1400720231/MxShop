from __future__ import unicode_literals

import math

from django.http import JsonResponse
from django.utils import six
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from rest_framework import status
from rest_framework.compat import unicode_to_repr
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from rest_framework.exceptions import APIException


# 自定义错误返回的信息体
class NotAuthenticated(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('请登陆后在访问')
    default_code = 'not_authenticated'
