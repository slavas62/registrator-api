from . import *

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'color': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(levelname)-8s %(message)s',
            'log_colors': {
                'DEBUG':    'bold',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'bold_red',
            },
        },
        'color_no_level': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(message)s',
            'log_colors': {
                'DEBUG':    'bold',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'bold_red',
            },
        },
        'db_color_no_level': {
            '()': 'main.contrib.logging.db.ColoredFormatter',
            'format': '%(log_color)s%(message)s',
            'log_colors': {
                'FAST':     'green',
                'MEDIUM':   'yellow',
                'SLOW':     'red',
            },
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'stdout': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
        'cmd': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'color'
        },
        'cmd_no_level': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'color_no_level'
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'app.log'),
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'db_color_no_level': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'db_color_no_level'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['logfile'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django': {
            'handlers': ['logfile'],
            'propagate': True,
            'level': 'WARNING',
        },
        'django.db.backends': {
            'handlers': ['logfile'],
            'propagate': True,
            'level': 'WARNING',
        },
        'console': {
            'handlers': ['cmd'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'console_no_level': {
            'handlers': ['cmd_no_level'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'db_color_no_level': {
            'handlers': ['db_color_no_level'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}