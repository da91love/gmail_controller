
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
from api_gmail_sender.type.ResType import ResType
from common.lib.ma.data_access.system.AccessService import AccessService
from common.const.SLACK import *
from common.slack.Slack import Slack
from common.slack.SlackMsgCreator import SlackMsgCreator

# Create instance
config = get_config()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def app_api_kpi_checker(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    data = event
    pic_email_matches = AccessService.select_pic_email_match()

    # 연락횟수 count
    cnct_num_sum = 0
    today = datetime.now().strftime('%Y-%m-%d')
    for pic_email_match in pic_email_matches:
        sender_email = pic_email_match['sender_email']

        contacts_by_sender_email = AccessService.select_today_contacts(
            today=today,
            sender_email=sender_email
        )

        cnct_num_sum += len(contacts_by_sender_email)

    # 계약횟수 count
    delivery_num = len(AccessService.select_delivery_info_master(today=today))

    # 새로보낸 메일수
    today_contact_num = len(AccessService.select_keyword_master(today=today))

    post_msg = SlackMsgCreator.get_slack_kpi_post_block(
        today=today,
        today_contact_count=today_contact_num,
        cnct_count=cnct_num_sum,
        delivery_count=delivery_num,
    )

    # declare instance
    slack = Slack()

    slack.add_post(SLACK_GLOBAL_SEEDING_CHANNEL_ID, MSG_TYPE['BLOCK'], post_msg)


    return ResType(data={}).get_response()

result = app_api_kpi_checker(None)
print(result)

