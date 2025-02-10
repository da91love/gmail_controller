
# import boto3
import csv
import uuid
from datetime import datetime
from operator import itemgetter
import pydash as _
from googleapiclient.errors import HttpError
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(api_root)

import pydash as _
from common.AppBase import AppBase
from common.util.get_config import get_config
from api_tiktok_posts_info.type.ResType import ResType
from api_slack_alerter.const.SLACK_ALERTER_TYPE import *
from api_slack_alerter.alerters.alert_new_invoice import alert_new_invoice
from api_slack_alerter.alerters.alert_new_buyer import alert_new_buyer
from api_slack_alerter.alerters.alert_new_order import alert_new_order

# Create instance
config = get_config()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def app_api_slack_alerter(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    data: dict = event

    slack_alerter_type, payload = itemgetter('slack_alerter_type', 'payload')(data)

    if slack_alerter_type == NEW_BUYER_ALERTER:
        alert_new_buyer(payload)
    elif slack_alerter_type == NEW_INVOICE_ALERTER:
        alert_new_invoice(payload)
    elif slack_alerter_type == NEW_DELIVERY_REQUEST_ALERTER:
        alert_new_order(payload)

    return ResType(data={}).get_response()