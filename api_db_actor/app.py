
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
from api_db_actor.const.DB_TYPE import *
from api_db_actor.actor.insert_invoice_master import insert_invoice_master

# Create instance
config = get_config()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def api_db_actor(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    data: dict = event

    db_type, payload = itemgetter('db_type', 'payload')(data)

    if db_type == INVOICE_MASTER:
        insert_invoice_master(payload)

    return ResType(data={}).get_response()