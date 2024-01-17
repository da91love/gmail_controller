import os
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = {
    'name': 'development',
    'DB': {
            'mysql': {
                'db_host': '3.36.197.228',
                'db_database': 'mna',
                'db_port': '3306',
                'db_user': 'mna',
                'db_password': 'mna11!!',
                'ssl_disabled': True
            }
    },
    'AMZN': {
        'refresh_token': 'Atzr|IwEBIJF8jjpLK8fxPoimh3QCM6DSd1rQVD5llNKx67E0kxPYsn7CZlJmv9Vr1t8VZW3v8SBTbPb6tocZK2wtc8hpIqliWRkGNoJxLrBkt7XlmtIzh03BBfRfntlz7-1_CoTzvBZViTdMjYB7yXw9OHhIbZdG2u4vL_KbTmoH2GnNDweLTGUkdGw9mokP45BkfPAWshYVrm3CHIuQyjCpHDW1Q4jLJ8T2MfRH2IH8o1kIsrPdtMH8dX56f21S9t1tV1PhAby9XmiJ-hgNwrjW9Yq2Njgf2uaq_JvsWBvoYlxYVFs-Eia0f8kNJDUOF5APFZzfyTQ',
        'client_id': 'amzn1.application-oa2-client.71eccd90ab3b4ed48a5cb7853d7db7f3',
        'client_secret': 'amzn1.oa2-cs.v1.c9a9346ef9605297d55dcc3e48795ada9f9b74ea51a2bad17ddb9363b3e0391a'
    },
    'LOG_CONFIG': {
        'version': 1,
        'formatters': {
            'general': {
                'format': '[%(asctime)s %(levelname)8s] %(filename)s %(funcName)s at line %(lineno)s - %(message)s'
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
                'mode': 'w',
                'encoding': 'utf-8',
                'formatter': 'general',
                'level': 'INFO',
            },
            'errorFile': {
                'class': 'logging.FileHandler',
                'filename': project_root + '/log/errorLogfile.log',
                'mode': 'w',
                'encoding': 'utf-8',
                'formatter': 'general',
                'level': 'ERROR',  # Set the level to capture only ERROR messages
            }
        },
        'root': {
            'handlers': ('console', 'file', 'errorFile'),
            'level': 'INFO'
        },
    },
}