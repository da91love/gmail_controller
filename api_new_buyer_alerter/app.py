
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
from common.tiktok.get_post_stat import get_post_stat
from common.slack.Slack import Slack
from common.slack.SlackMsgCreator import SlackMsgCreator
from common.const.SLACK import *


# Create instance
config = get_config()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def app_api_new_buyer_alerter(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    data: dict = event

    corporate_name: str = data.get('corporate_name')
    business_name: int = data.get('business_name')
    country: str = data.get('country')
    pic: str = data.get('pic')
    url: str = data.get('url')
    mau: str = data.get('mau')

    slack = Slack()
    slack_msg = SlackMsgCreator.get_slack_new_buyer_post_block(
        corporate_name=corporate_name,
        business_name=business_name,
        country=country,
        url=url,
        mau=mau,
        pic=pic
    )

    slack.add_post(
        channel_id=SLACK_GLOBAL_EQB_CHANNEL_ID,
        msg_type=MSG_TYPE['BLOCK'],
        msg_body=slack_msg
    )

    return ResType(data={}).get_response()