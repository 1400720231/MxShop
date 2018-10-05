from django.shortcuts import render

# Create your views here.
from .models import Goods
from goods.serializer import GoodsSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework import viewsets

class GoodstListView(APIView):
    """
    这里是对GoodstListView的解释信息，在浏览器可以看到这条信息
    """
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