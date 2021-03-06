# -*- coding: utf-8 -*-
"""
Django settings for happyhouse project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@r#hu@cc37w@mkh4nrn_k=*jir55ouu6x&c#oe=&4kk_f$#x*4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'boss',
    'html5helper',
    'smart_auth',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'happyhouse.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'happyhouse.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'happyhouse',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '123456',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# 这个是菜单，只支持2级菜单
MENUS = [
    {"text": u"能力模型", "url":"", "children": [
        {"text": u"能力类型", "url": "Category"},
        {"text": u"题库管理", "url": "Problem"},
        {"text": u"试卷管理", "url": "Paper"},
        {"text": u"我的题目", "url": "ProblemMy"},
        {"text": "divider", "url": "_", "divider": True},  #这个是分割线
        {"text": u"历史评测", "url": "Exam"},
        {"text": u"安排评测", "url": "ExamStart"},
    ]},
    {"text": u"服务器授权", "url":"", "children": [
        {"text": u"密钥管理", "url": "CodePublicKey"},
        {"text": "divider", "url": "_", "divider": True},
        {"text": u"服务器", "url": "Server"},
        {"text": u"授权日志", "url": "ServerInstallLog"},
    ]},
    {"text": u"市场营销", "url":"", "children": [
        {"text": u"机会管理", "url": "Customer"}
    ]},

    {"text": u"系统管理", "url":"", "children": [
        {"text": u"公司管理", "url": "Company"},
        {"text": u"部门管理", "url": "Department"},
        {"text": u"岗位管理", "url": "Position"},
        {"text": u"项目管理", "url": "Project"},
        {"text": u"人员管理", "url": "User"},
        {"text": u"权限管理", "url": "UserPermission"},
        {"text": u"人员组管理", "url": "UserGroup"},
        {"text": "divider", "url": "_", "divider": True},
        {"text": u"人员支出", "url": "UserExpense"},
        {"text": u"项目支出", "url": "ProjectExpense"},
    ]},
]

# API的代码目录
APIS_DIR = os.path.join(BASE_DIR, "smart_auth/apis/")
APIS_PREFIX = "smart_auth.apis"

