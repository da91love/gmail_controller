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
    'TIKAPI': {
        'api_key': 'enee9qPIfAc0B3INftVKZCMnWvOPqivueTzFM87d4mRmNr1e',
        'account_key': 'lcg6taQkMqXHP6CntOnH67qxEAoiaMJXLKu5kREdp9GXzerx'
    },
    'AMZN': {
        'refresh_token': 'Atzr|IwEBIFC_OYwgw4WFb0cNDvHmLXE-Wi2Y3o-rKn86HwqT3cOfHVULKVNHqMTp88B5tZXGsEN0fQb06EgBHX2cxD_WOxSeETEboHU3CxIsboPxgtmbHOT3_NPCmTjLDBPPCNl9S9q61fuTxkixSa0EeVkjdvjQwWt82FAkEr5RdGf6kp3w1r1fs-xlr2xZpBvl90hh4_pQx6qbTxLrgs8QTiTXd_MR2BnP6QUbEV64MdE4-JIRNefUT1yK26U_e9zbKYWDkQTmtFVRisVD_dndQMziPZPOuGkwca1S9xf0tjvP670A8bQnC7GRzQbfRf9G962_O5MtPXbPdTdKFsyFXz---_Sp2XciGa4DAYlZ5cBJ_qmxQA',
        'client_id': 'amzn1.application-oa2-client.a143a078306b4e65a2e22722b9c98294',
        'client_secret': 'amzn1.oa2-cs.v1.a76af9ae56620b01a852a32952cfc62f15e02b2c01d080910283f4fb2dcb27c6'
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