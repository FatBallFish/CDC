"""
Django settings for CDC project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=8-ccu7k(9d=noztc7+2o5rjy(xj5_!=g^bkx%0-!$*3#34hul'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "guosai.zustmanong.cn", "guosai.zustmanong.cn"]

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'apps.realauth.apps.RealauthConfig',
    # 'apps.operation.apps.OperationConfig',
    'apps.users.apps.UsersConfig',
    'apps.tokens.apps.TokensConfig',
    'apps.recommend.apps.RecommendConfig',
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

ROOT_URLCONF = 'CDC.urls'

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

WSGI_APPLICATION = 'CDC.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'guosai',
        'USER': 'guosai',
        'PASSWORD': 'guosai2020',
        'HOST': '5780e03864e11.sh.cdb.myqcloud.com',
        'PORT': 4201,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # 注意:这里配置os的时候,不像配置static的时候要[],这里不需要[]
MEDIA_URL = "/media/"
API_ROOT = 'api/'

# Redis
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASS = "foobared"
REDIS_IMG_SETNAME = "img_authentication"
REDIS_SMS_SETNAME = "sms_authentication"
REDIS_CHECKIN_SETNAME = "checkin_authentication"
# SMS
SMS_APPID = "1400097031"
SMS_APPKEY = "417a2a23700289bf50f6cff4fdefa467"
# COS
COS_SECRET_ID = "AKIDBA5ss1AJZZloVP4la9SWpMC6wXtzqNfi"
COS_SECRET_KEY = "A9yjEUcmhMmaCYf3SjwyBSjZZUOAh0GW"
COS_REGION = "ap-shanghai"
COS_BUCKET = "hotel-1251848017"
COS_ALLOWURL = "http://127.0.0.1,http://localhost"
COS_ROOTURL = "https://hotel-1251848017.cos.ap-shanghai.myqcloud.com/"
COS_SERVER_MODE = 1
COS_CACHE_TIME = 3
# simpleui
SIMPLEUI_DEFAULT_THEME = 'admin.lte.css'
# SIMPLEUI_HOME_PAGE = 'https://www.baidu.com'
# SIMPLEUI_HOME_TITLE = '酒店视觉AI解决方案-后台管理'
SIMPLEUI_HOME_INFO = False  # 服务器信息,右侧simple ui主页
SIMPLEUI_ANALYSIS = False

# import-export
IMPORT_EXPORT_USE_TRANSACTIONS = True  # 使用数据库事务，确保数据安全
