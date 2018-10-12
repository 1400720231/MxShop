"""
Django settings for MxShop project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# 表示最外面的那个MxShop文件夹的路径,注意是路径.,不是文件夹的名字.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 把第三方路插入django项目文件环境路径,可直接import apps中的包 而不用from apps import ...
# sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q6_qmf801@5%6-752^76))8yr%a4@^flk^igrz&p-@rvc5_3pp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# 用自定义的用户数据表替换系统自带user信息表
AUTH_USER_MODEL = 'users.UserProfile'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'DjangoUeditor',
    'users',
    'goods',
    'trade',
    'user_operation',
    'xadmin',
    'crispy_forms',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MxShop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MxShop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'mxshop',
        'HOST':'localhost',
        'USER':'root',
        'PASSWORD':'root',
        'PORT':'3306',
        'OPTIONS':{'init_command':'SET default_storage_engine=INNODB;'}
    }
}
"""
MyISAM是mysql默认的存储引擎,这里用下面命令修改mysql储存引擎,主要是考虑到后面
有一个第三方登陆的数据表需要这个储存引擎,不然到时候数据迁移的时候会报错
mysql 5.6以上为default_storage_engine
'OPTIONS':{'init_command':'SET default_storage_engine=INNEDB;'}


"""

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False # 默认是True,时间是utc时间,由于我们要用本地时间,所有false


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]


MEDIA_URL = '/media/'  # 不能随便取 因为用的时候src="{{MEDIA_URL}}/image/..."表示按照这个路径找
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
"""
MEDIA_ROOT只能设置一个，不然她不知道到底存放再哪里，和static不同，static是准备取出来用的，可以到设置的目录里找就行了，
但是MEDIA_ROOT是为了保存上传文件的地方，你要是设置多个，他不晓得存在什么地方。可以，没毛病！
"""



"""
drf 全局配置:REST_FRAMEWORK配置，比如分页等。
但是当在serilizer中自定义pagination_class后，在
全局的REST_FRAMEWORK配置就不需要配置DEFAULT_PAGINATION_CLASS了
"""

# REST_FRAMEWORK = {
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
#     'PAGE_SIZE': 10 # 每个10个，注意如果你的数据不多，只够一页数据的话，browser页面是没有分页栏显示的
#
# }