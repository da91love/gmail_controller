
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

from common.AppBase import AppBase
from common.util.get_config import get_config
from api_tiktok_posts_info.type.ResType import ResType
from common.tiktok.get_posts import get_posts


# Create instance
config = get_config()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def app_api_tiktok_posts_info(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    data = event
    uniq_id: str = data.get('uniqId')
    period: int = data.get('period')

    result = get_posts(uniq_id=uniq_id, day_bf_until=period)

    return ResType(data=result).get_response()

# uniqId = sys.argv[1]
# period = sys.argv[2]
#
# result = app_api_tiktok_posts_info({
#     "uniqId": uniqId,
#     "period": period
# })
# print(result)

