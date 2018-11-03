from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

"""
    此方法是调用django的信号机制来完成密码的加密。因为serializer中的字段验证通过后会直接
存入数据库，不会加密，其中一种方式就是重载ModelSerializer中的cerate方式进行操作加密，
    第二种方式就是利用这里的django信号机制来完成密码的加密，当model进行数据库操作的时候，
django会给全局发送一个信号，这就是截获这个信号然后做处理。

在这里写好对应的函数后，记得在对应的应用apps.py下面添加如下内容：
        def ready(self):
            import users.signals

添加前的：      
class UsersConfig(AppConfig):
    name = 'users'
    verbose_name='用户信息'

   
添加后的：
class UsersConfig(AppConfig):
    name = 'users'
    verbose_name='用户信息'

    def ready(self):
         # 导入写有信号函数的py文件
        import users.signals
"""
# 因为我采用了方式一重载ModelSerializer中的create方式来实现，这里就注释了

# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     """
#     :param sender:
#     :param instance: 就是model中修改的那个实例（创建或者修改）
#     :param created: 是否为创建
#     :param kwargs:
#     :return:
#     """
#     if created:
#         password = instance.password
#         instance.set_password(password)
#         instance.save()