from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name='用户信息'

    def ready(self):
        # 导入写有信号函数的py文件
        import users.signals