import logging

import sys
from .log_filters import ErrorLogFilter, InfoLogFilter, DebugWarningLogFilter

logging_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
        },
    'filters': {
        'info_filter': {
            '()': InfoLogFilter,
        },
        'debug_warning_filter': {
            '()': DebugWarningLogFilter,
        },
        'error_filter': {
            '()': ErrorLogFilter,
        },
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'stderr': {
            'class': 'logging.StreamHandler',
        },
        'stdout': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'filters': ['debug_warning_filter'],
            
        },
        'error_file': {
            'class': 'logging.FileHandler',
            'filename': 'error.log',
            'mode': 'w',
            'level': 'ERROR',
            'formatter': 'default',
            'filters': ['error_filter']
        },
        'info_file': {
            'class': 'logging.FileHandler',
            'filename': 'info.log',
            'mode': 'w',
            'level': 'INFO',
            'formatter': 'default',
            'filters': ['info_filter']
        },
    },
    'loggers': {
        '': {  
            'handlers': ['default', 'stdout', 'error_file', 'info_file'],
            'level': 'DEBUG',  
            'propagate': True,
        },
    },
    }