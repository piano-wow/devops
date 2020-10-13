"""
Django settings for devops project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
在使用 celery beat 时发现 django 配置参数名只能使用大写
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# app统一放到apps目录，方便管理
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
if not os.path.isdir(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)
MEDIA_URL = '/media/'

RECORD_DIR = 'record'   # 存放终端结果文件
RECORD_ROOT = os.path.join(MEDIA_ROOT, RECORD_DIR)
if not os.path.isdir(RECORD_ROOT):
    os.makedirs(RECORD_ROOT)

SCRIPT_DIR = 'script'   # 存放脚本
SCRIPT_ROOT = os.path.join(MEDIA_ROOT, SCRIPT_DIR)
if not os.path.isdir(SCRIPT_ROOT):
    os.makedirs(SCRIPT_ROOT)

GUACD_DIR = 'guacd'     # guacd 挂载目录，用于 rdp 下载上传文件
GUACD_ROOT = os.path.join(MEDIA_ROOT, GUACD_DIR)
if not os.path.isdir(GUACD_ROOT):
    os.makedirs(GUACD_ROOT)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

TMP_DIR = 'tmp'
TMP_ROOT = os.path.join(MEDIA_ROOT, TMP_DIR)
if not os.path.isdir(TMP_ROOT):
    os.makedirs(TMP_ROOT)

FILE_UPLOAD_MAX_MEMORY_SIZE = 27262976    # 上传的文件保存在内存中的大小限制  26MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 27262976    # 上传的数据保存在内存中的大小限制  26MB

FILE_UPLOAD_TEMP_DIR = os.path.join(MEDIA_ROOT, 'tmp')       # 上传的文件大于FILE_UPLOAD_MAX_MEMORY_SIZE时临时保存目录

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jp9kd-^-)93ke1^4i6)sd^+kovh2)197m83+^q+o_6^+dz^3xb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    # 'simpleui',
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'debug_toolbar',
    'cachalot',
    'channels',
    'server',
    'user',
    'webssh',
    'webtelnet',
    'webguacamole',
    'tasks',
    'batch',
    'scheduler'
    # 'django_apscheduler',
]

# django-cachalot 原理是捕获 insert\update\delete 操作而刷新缓存，如果不是通过 django orm，而是直接改的数据库，那么就不能触发其缓存
# 刷新机制，这是可以使用其提供的手动刷新命令解决：./manage.py invalidate_cachalot [app]
# 具体参考文档：https://django-cachalot.readthedocs.io/en/latest/quickstart.html#manage-py-command
# 并且 django-cachalot 不适用于 insert\update\delete 操作很频繁的项目，这种项目反而会使其性能下降
CACHALOT_ENABLED = True     # 不懂官方这个配置什么意思，设置 False 还是会启用缓存
CACHALOT_DATABASES = ['default']    # 需要缓存的数据库别名，必须设置，默认的 supported_only 只支持 django 默认的数据库引擎，不支持自定义的 db_pool.mysql 连接池引擎
# 更多配置参考：https://django-cachalot.readthedocs.io/en/latest/quickstart.html#settings

# 中间件
MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'util.middleware.NewNextMiddleware',
    'util.middleware.GetRealClientMiddleware',  # 前端有代理，获取真实 IP
    # 'util.middleware.BlackListMiddleware',  # IP 黑名单
    'util.middleware.LockScreenMiddleware',     # 锁屏
    # 'util.middleware.DebugMiddleware',      # 非 DEBUG 模式下管理员显示 DEBUG 页面
    'util.middleware.PermissionMiddleware',      # 验证权限
]

# DEBUG_TOOLBAR_PANELS = [
#     'debug_toolbar.panels.versions.VersionsPanel',
#     'debug_toolbar.panels.timer.TimerPanel',
#     'debug_toolbar.panels.settings.SettingsPanel',
#     'debug_toolbar.panels.headers.HeadersPanel',
#     'debug_toolbar.panels.request.RequestPanel',
#     'debug_toolbar.panels.sql.SQLPanel',
#     'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     'debug_toolbar.panels.templates.TemplatesPanel',
#     'debug_toolbar.panels.cache.CachePanel',
#     'debug_toolbar.panels.signals.SignalsPanel',
#     'debug_toolbar.panels.logging.LoggingPanel',
#     'debug_toolbar.panels.redirects.RedirectsPanel',
#     'debug_toolbar.panels.profiling.ProfilingPanel',
#     'cachalot.panels.CachalotPanel',
# ]
#
# INTERNAL_IPS = [
#     # ...
#     '172.17.0.1',
#     '127.0.0.1',
#     '192.168.223.1',
#     '192.168.223.2',
#     # ...
# ]

FILE_UPLOAD_HANDLERS = [
    # 'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]


# 添加 websocket 支持
ASGI_APPLICATION = 'devops.routing.application'

ROOT_URLCONF = 'devops.urls'

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

WSGI_APPLICATION = 'devops.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES_sqlite = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.mysql',
        'ENGINE': 'db_pool.mysql',     # 重写 mysql 连接库实现连接池
        'NAME': 'devops',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '192.168.223.111',
        'PORT': '3306',
        # 'CONN_MAX_AGE': 600,    # 如果使用 db_pool.mysql 绝对不能设置此参数，否则会造成使用连接后不会快速释放到连接池，从而造成连接池阻塞
        # 数据库连接池大小，mysql 总连接数大小为：连接池大小 * 服务进程数
        'DB_POOL_SIZE': 3,     # 默认 5 个
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
         },
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# simpleui 使用本地css和js
# SIMPLEUI_STATIC_OFFLINE = True

# session 如果在此期间未做任何操作，则退出， django 本身要么设置固定时间，要么关闭浏览器失效
CUSTOM_SESSION_EXIPRY_TIME = 60 * 30    # 秒

# 终端过期时间，最好小于等于 CUSTOM_SESSION_EXIPRY_TIME
CUSTOM_TERMINAL_EXIPRY_TIME = 60 * 15      # 秒

REDIS_SETTING = {
    'host': '192.168.223.111',
    'port': 6379,
}

# celery 配置 redis
CELERY_BROKER_URL = 'redis://{0}:{1}/0'.format(REDIS_SETTING['host'], REDIS_SETTING['port'])
# beat 中 Scheduler 循环调度任务的最大等待时间(s)
CELERY_BEAT_MAX_LOOP_INTERVAL = 10
# RedisMultiScheduler 利用 redis 实现 beat 的动态添加，修改，删除任务
CELERY_BEAT_SCHEDULER = 'redismultibeat.RedisMultiScheduler'
CELERY_BEAT_REDIS_SCHEDULER_URL = 'redis://{0}:{1}/0'.format(REDIS_SETTING['host'], REDIS_SETTING['port'])
CELERY_BEAT_REDIS_SCHEDULER_KEY = 'devops:celery:beat:tasks'
# redis 锁，实现运行多个 beat 实例而不会重复执行任务， beat 官方只能运行一个实例
CELERY_BEAT_REDIS_MULTI_NODE_MODE = True      # 是否开启多实例模式
CELERY_BEAT_REDIS_LOCK_KEY = 'devops:celery:beat:lock'
CELERY_BEAT_REDIS_LOCK_TTL = 5
# 多实例模式下，未获取到锁的实例等待多长时间(s)再试，如果设置为 None 或者不设置,
# 则会随机等待 1 - CELERY_BEAT_REDIS_LOCK_TTL 之间的一个值，设置越小丢失任务的
# 可能性越低，但是对 redis 的性能消耗也越高，根据实际情况权衡
CELERY_BEAT_REDIS_LOCK_SLEEP = None

from datetime import timedelta
from celery.schedules import crontab
"""
celery beat 中间隔时间任务有个小问题，比如任务10秒间隔执行，则执行时间会如下：
2019-12-04 13:20:38,105
2019-12-04 13:20:48,125
2019-12-04 13:20:58,143
2019-12-04 13:21:08,160
2019-12-04 13:21:18,179
2019-12-04 13:21:28,199
2019-12-04 13:21:38,203
...
2019-12-07 13:21:39,008
你会发现每次执行时间都会延迟 10-30 毫秒之间（程序执行逻辑耗费的时间），如果任务有严格时间要求，则不适合使用这种类型的任务
cron 任务暂时没发现这个问题
"""
# 启动 beat 时是否清空已有任务
CELERY_BEAT_FLUSH_TASKS = True

CELERY_BEAT_SCHEDULE = {    # celery 定时任务, 会覆盖 redis 当中相同任务名任务
    # 'task_check_scheduler_interval': {  # 任务名(随意起)
    #     'task': 'tasks.tasks.task_check_scheduler',  # 定时任务函数路径
    #     'schedule': timedelta(seconds=30),  # 任务循环时间
    #     # "args": None,  # 参数
    #     "args": (None, 0, 3),  # 参数
    # },
    # 'task_check_scheduler_cron': {
    #     'task': 'tasks.tasks.task_check_scheduler',
    #     'schedule': crontab(minute='*/1', hour='*', day_of_week='*', day_of_month='*', month_of_year='*'),  # cron 任务
    #     # "args": None,  # 参数
    #     "args": (None, 0, 3),  # 参数
    # },
    'task_cls_terminalsession': {   # 清除 terminalsession 表，系统异常退出时此表可能会有垃圾数据，仅启动时运行一次
        'task': 'tasks.tasks.task_cls_terminalsession',
        'schedule': timedelta(seconds=3),
        "limit_run_time": 1,   # 限制任务执行次数，>=0, 0 为不限制。注意：celery 原版 beat 是不支持此参数的
    },
}

# channels channel_layers 使用 redis
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_SETTING['host'], REDIS_SETTING['port'])],
        },
    },
}

# 缓存使用 redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{0}:{1}'.format(REDIS_SETTING['host'], REDIS_SETTING['port']),
        'OPTIONS': {
            # 'DB': 10,
            # 'PASSWORD': '123456',
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 150,
                'timeout': 15,
            },
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",   # 开启压缩
        },
        'KEY_PREFIX': 'devops',
    }
}

# SESSION_ENGINE = "django.contrib.sessions.backends.cached_db" # 使用数据库，比较慢
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'   # 使用 CACHES 设置的 redis
SESSION_COOKIE_HTTPONLY = True

# proxy_sshd 监听配置
PROXY_SSHD = {
    'listen_host': '0.0.0.0',
    'listen_port': 2222,
    'cons': 150,
}

# guacd 配置
GUACD = {
    'host': '192.168.223.111',
    'port': 4822,
    'timeout': 15,
}

# 访问黑名单， 需开启 Middleware：util.middleware.BlackListMiddleware
BLACKLIST = ['192.168.223.220', '192.168.223.221']

# ansible 变量禁止名单，防止执行 ansible 任务时使用类似 {{ ansible_ssh_pass }} 获取到主机密码
ANSIBLE_DENY_VARIBLE_LISTS = [
    "vars",
    "hostvars",
    "ansible_ssh_pass",
    "ansible_password",
    "ansible_ssh_private_key_file",
    "ansible_private_key_file",
    "ansible_become_pass",
    "ansible_become_password",
    "ansible_enable_pass",
    "ansible_pass",
    "ansible_sudo_pass",
    "ansible_sudo_password",
    "ansible_su_pass",
    "ansible_su_password",
    "vault_password",
]

# ansible 连接插件 connection 的连接类型, 有 ssh, paramiko, smart 等，ansible 默认 smart
# 详情参考 https://docs.ansible.com/ansible/latest/plugins/connection.html
ANSIBLE_CONNECTION_TYPE = 'paramiko'


# django-ratelimit 限制页面访问频率，超过则返回 403
# None 表示无限制，具体见 https://django-ratelimit.readthedocs.io/en/stable/rates.html
# RATELIMIT_LOGIN = None
RATELIMIT_LOGIN = '600/30s'
RATELIMIT_NOLOGIN = '30/30s'


# 用户加密密钥
# 第一次设置后切勿再随意更改
PASSWD_TOKEN = '__leffss__qaz__devops'


# cryptography 加密解密密钥
# 生成方法：
# from cryptography.fernet import Fernet
# cipher_key = Fernet.generate_key()
# 非常重要，修改后会便无法解密数据库中储存的主机密码，所以第一次生成后切勿再随意更改
CRYPTOGRAPHY_TOKEN = 'a0pLIWQvKYXp27uhQ7Bm5MDnQPvYSJ2oLaDZ6gJ_EJs='


# 权限和菜单 key ，用于设置 session
INIT_PERMISSION = 'devops_init_permission'
INIT_MENU = 'devops_init_menu'
VALID_URL = [   # 白名单url，不做权限验证
    '/',
    '/user/login/',
    '/user/logout/',
    '/user/lockscreen/',
    '/user/profile/',
    '/user/profile/edit/',
    '/api/user/password/update/',
    '/api/user/profile/update/',
    '/api/scheduler/client/upload/',
]
