# import boto3
import csv
import uuid
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
def app_api_delivery_tracker(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    eventdata = event

    tracking_tg_invoices = AccessService.select_delivery_info()

    result = []
    try:
        tw_amz = TrackingWrapper(COURIER['AMAZON'], tracking_tg_invoices)
        result += tw_amz.update_tracking_history()
    except AmzApiAuthenticationException:
        pass

    try:
        tw_rcs  = TrackingWrapper(COURIER['RINCOS'], tracking_tg_invoices)
        result += tw_rcs.update_tracking_history()
    except Exception as e:
        raise e

    return ResType(data=result).get_response()

# result = app_api_delivery_tracker(None)
# print(result)