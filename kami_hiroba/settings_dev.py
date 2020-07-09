from .settings_common import *


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True


# 送信したメールをコンソールに表示(実際には送信しない)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# 開発中のメディアルート

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# django-debug-toolbar 設定

INTERNAL_IPS = [
    '127.0.0.1',
]


# ログ設定

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'hiroba': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },

    'handlers': {
        'console': {
            'level': DEBUG,
            'class': 'logging.StreamHandler',
            'formatter': 'dev'
        },
    },

    'formatters': {
        'dev': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d',
                '%(message)s'
            ])
        },
    }
}
