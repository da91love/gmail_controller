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
        'refresh_token': 'Atzr|IwEBIKNZZj1dxfn2zWV2BFFxTYhqtl8HUXoOsHIF5LuICWpAb-5LdKIoX9TinwO2b7Qal0NScpIEszu6UA312y_M5v76OvuN4RZCkSjFk0DJZptByp5d0TAzqhxgJn5PuQmjS4ny4yR_eyTkzlyKPFQdaP9csc_eUlbpahM-1vdp3btDGC3_hmRqA_UG0ECy63pgWxdSEDRaH3Bj0y27X7JIIpywMFCBnAPLOGZiXuPS8dUN36PHuZbA4gyc6CHPfdsBb8aSWJk-iT3hWWQV2Q0v_TbNmWnwsfhrKO6QKVdBM0UXgu8vb6feFMc-fKvA-9R7wT4',
        'client_id': 'amzn1.application-oa2-client.71eccd90ab3b4ed48a5cb7853d7db7f3',
        'client_secret': 'amzn1.oa2-cs.v1.f4e48f52a9a19210e75a84fe17130d66b53da85ff04ff3cd2b1c87a5899b2793'
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
        },
        'root': {
            'handlers': ('console', 'file'),
            'level': 'INFO'
        },
    },
}