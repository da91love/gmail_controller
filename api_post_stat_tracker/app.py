# import boto3
import csv
import uuid
from tikapi import TikAPI, ValidationException, ResponseException
import os
import sys
from mysql.connector.errors import *
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(api_root)

from api_gmail_checker.type.ResType import ResType
from common.AppBase import AppBase
from common.type.Errors import *
from common.util.get_config import get_config
from common.util.logger_get import get_logger
from common.scm.TrackingWrapper import TrackingWrapper
from common.scm.amazon.Amazon import Amazon
from common.scm.rincos.Rincos import Rincos
from common.lib.ma.data_access.system.AccessService import AccessService
from common.const.SCM import COURIER

# Create instance
config = get_config()
logger = get_logger()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def app_api_post_stat_tracker(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    eventdata = event

    # config data
    api_key = config['TIKAPI']['api_key']
    account_key = config['TIKAPI']['account_key']

    # declare instance
    api = TikAPI(api_key)
    User = api.user(accountKey=account_key)

    try:
        response = User.posts.video(
            id="7327368161349913902"
        )

        res = response.json()
        print(res)

    except ValidationException as e:
        print(e, e.field)

    except ResponseException as e:
        print(e, e.response.status_code)

    return ResType(data=result).get_response()

# result = app_api_delivery_tracker(None)
# print(result)