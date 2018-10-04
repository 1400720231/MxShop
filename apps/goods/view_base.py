from goods.models import Goods
from django.views.generic.base import View
from django.http import HttpResponse
import json
from django.forms.models import model_to_dict

"""
序列化方式一：原声django方式
缺点：
    赋值麻烦，而且ImgaeField DateTime等字段不能序列化
class GoodList(View):
    def get(self, request):
        json_list = []
        goods = Goods.objects.all()[:5]
        for good in goods:
            json_dict = {}
            json_dict['name'] = good.name
            json_dict['category'] = good.category.name
            json_dict['market_price'] = good.market_price
            # DateTime不能用json序列化
            # json_dict['add_time'] = good.add_time
            json_dict['xxx'] = good.goods_brief
            json_list.append(json_dict)

        return HttpResponse(json.dumps(json_list),content_type='application/json')
"""

"""
序列化方式二：原声django方式+model_to_dict
有点：
    model_to_dict让序列化更方便，不用挨个赋值：json_dict['name'] = good.name
缺点：
    ImgaeField DateTime等字段不能序列化
class GoodList(View):
    def get(self, request):
        json_list = []
        goods = Goods.objects.all()[:5]
        for good in goods:
            json_dict = model_to_dict(good)
            del json_dict['goods_front_image']
            del json_dict['add_time']
            json_list.append(json_dict)

        return HttpResponse(json.dumps(json_list),content_type='application/json')
"""


# 序列化方式三：原声django方式+django自带serializers
# 优点：可以序列化所有字段
# 缺点：ImageField这种类型显示一般的路径："goods/images/1_P_1449024889889.jpg"
#       而不现实完整路径127.0.0.1：8000/goods/images/1_P_1449024889889.jpg
#       并且外键字段序列化的是id而不是外键对应model中的def __str__():return self.name字段
from django.core import serializers
class GoodList(View):
    def get(self, request):
        goods = Goods.objects.all()[:5]
        json_data = serializers.serialize('json',goods)

        return HttpResponse(json_data,content_type='application/json')


"""
drf 可以解决上面所有问题：
    DateTime 可以成功序列化
    ImageField这种字段的序列化可以显示全部路径
    category外键字段的序列化都可以成功序列化

而且drf的功能远不止这些，所以这就是用drf的原因。
"""