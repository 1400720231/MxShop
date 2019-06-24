import xadmin

from .models import GoodsCategory, GoodsCategoryBrand
from .models import Goods, GoodsImages, Banner,PandaTest


"""
# Course表单注册
class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'get_zj_nums', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
  
xadmin.site.register(BannerCourse, BannerCourseAdmin)
"""


class GoodsCategoryAdmin(object):
    list_display = ['name','desc','code','category_type','parents_category','is_tab','add_time']
    search_fields = ['name','desc','code','category_type','parents_category','is_tab','add_time']
    list_filter = ['name','desc','code','category_type','parents_category','is_tab','add_time']


class GoodsCategoryBrandAdmin(object):
    list_display = ['category','name','desc','image','add_time']
    search_fields =['category','name','desc','image','add_time']
    list_filter = ['category','name','desc','image','add_time']

    """
      只返回第一类数据，选的时候方便点，在GoodsCategoryBrand中有个外键category,
    这里context['form'].fields['category'].queryset的方式指明后台添加GoodsCategoryBrand的
    时候category不是显示所有的数据，而是显示第一类的数据：GoodsCategory.objects.filter(category_type=1)
    """

    def get_context(self):
        context = super(GoodsCategoryBrandAdmin, self).get_context()
        if 'form' in context:
            context['form'].fields['category'].queryset = GoodsCategory.objects.filter(category_type=1)
        return context


class GoodsAdmin(object):
    list_display = ['category', 'goods_sn', 'name', 'click_num', 'sold_num', 'fav_num', 'goods_num',
                    'market_price', 'shop_price', 'goods_brief', 'goods_desc', 'ship_free', 'goods_front_image',
                    'is_new', 'is_hot', 'add_time']
    search_fields = ['category', 'goods_sn', 'name', 'click_num', 'sold_num', 'fav_num', 'goods_num',
                    'market_price', 'shop_price', 'goods_brief', 'goods_desc', 'ship_free', 'is_new', 'is_hot', 'add_time']
    list_filter = ['category', 'goods_sn', 'name', 'click_num', 'sold_num', 'fav_num', 'goods_num',
                    'market_price', 'shop_price', 'goods_brief', 'goods_desc', 'ship_free', 'is_new', 'is_hot', 'add_time']

    # 在xadmin中一定要声明ueditor字段在models中的名字，比如这里的goods_desc
    style_fields = {"goods_desc": "ueditor"}


class GoodsImagesAdmin(object):
    list_display = ['goods','image','image_url','add_time']
    search_fields =['goods','image_url','add_time']
    list_filter = ['goods','image_url','add_time']


class BannerAdmin(object):
    list_display = ['goods','image','index','add_time']
    search_fields =['goods','image','index','add_time']
    list_filter = ['goods','image','index','add_time']


class PandaTestAdmin(object):
    list_display = ['name', 'age']


xadmin.site.register(GoodsCategory,GoodsCategoryAdmin)
xadmin.site.register(GoodsCategoryBrand,GoodsCategoryBrandAdmin)
xadmin.site.register(Goods,GoodsAdmin)
xadmin.site.register(GoodsImages,GoodsImagesAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(PandaTest, PandaTestAdmin)