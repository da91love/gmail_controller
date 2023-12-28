import os
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = {
    "name": "development",
    "DB": {
            "mysql": {
                "db_host": "3.36.197.228",
                "db_database": "mna",
                "db_port": "3306",
                "db_user": "mna",
                "db_password": "mna11!!",
                "ssl_disabled": True
            }
    },
    "LOG_CONFIG": {
        'version': 1,
        'formatters': {
            'general': {
                'format': "[%(asctime)s %(levelname)8s] %(filename)s %(funcName)s at line %(lineno)s - %(message)s"
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'general',
                'level': 'INFO',
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': project_root + '/log/logfile.log',
                'mode': 'a',
                'maxBytes': 10 * 1024 * 1024,  # 10 MB
                'backupCount': 5,
                'encoding': 'utf-8',
                'formatter': 'general',
                'level': 'INFO',
            },
        },
        'root': {
            'handlers': ('console', 'file'),
            'level': 'INFO'
        },
    },
}