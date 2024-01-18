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
        'refresh_token': 'Atzr|IwEBILT5klw3ky9rvvkTFd_qeQo5-bzWvAGy40jqu3OK8cJFxA78qi8wUkRal-EXjLABZ9qVKmHJejkYXhNclFCdom1rVfhXWVkIeElaVYDxil12i5FZhWPqjIRYmYa8MHH5oyrs6Diu2ET75xvpME4Lm88XXbdtHHB6efrzjI42zk3EnxuQ3itDE7HCJSb2mmBL4K4ghL-By2m0uF7L7hQA9WMaKZbhmE5W4dTk97OBbCcVXMaUjBWgrpG_dCgfD-_n4dYJLrLU4U2I2_EKZPY7HVf9gD2cFZSVGhuGcI3S7FyiGwouUITmir_o9QCphP4YvDviT7fZcgCH_Zb4LDei-6QBtSXHHkJtNPbQBTtzzL-Jiw',
        'client_id': 'amzn1.application-oa2-client.a143a078306b4e65a2e22722b9c98294',
        'client_secret': 'amzn1.oa2-cs.v1.894d9446a7b93c1ce56197abd74de800a55708bf0034198ef1975c5d15e04cfa'
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