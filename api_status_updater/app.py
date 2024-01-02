
# import boto3
import csv
import json
from operator import itemgetter
import os
import sys
from mysql.connector.errors import *
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(api_root)

from common.AppBase import AppBase
from common.type.Errors import *
from common.util.get_config import get_config
from api_gmail_checker.type.ResType import ResType
from common.slack.Slack import Slack
from common.const.SLACK import *
from common.slack.SlackMsgCreator import SlackMsgCreator
from common.lib.ma.data_access.system.AccessService import AccessService

# Create instance
config = get_config()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def lambda_handler(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    data = event

    # declare instance
    slack = Slack()

    # 10분이내 업데이트된 status 데이터 취득
    status_data = AccessService.select_status_in_10_min()

    # update slack
    updated_data = []
    for sd in status_data:
        gmail_thread_id = sd['gmail_thread_id']

        contact_data = AccessService.select_contacts(gmail_thread_id=gmail_thread_id)
        author_unique_id, seeding_num, tg_brand = itemgetter('author_unique_id', 'seeding_num', 'tg_brand')(contact_data[0])

        slack_need_info = AccessService.select_slack_need_info(author_unique_id=author_unique_id, seeding_num=seeding_num, tg_brand=tg_brand)[0]
        author_unique_id, receiver_email, tiktok_url, pic = itemgetter('author_unique_id', 'receiver_email', 'tiktok_url', 'pic')(slack_need_info)

        slack_id_info = AccessService.select_slack_thread_history(gmail_thread_id=gmail_thread_id)[0]
        slack_thread_id = itemgetter('slack_thread_id')(slack_id_info)

        status, progress = itemgetter('status', 'progress')(status_data[0])

        is_reply_done = True if contact_data[-1]['gmail_label_id'] == 'SENT' else False

        update_msg = json.dumps(SlackMsgCreator.get_slack_post_block(
            TIKTOK_URL= tiktok_url,
            AUTHOR_UNIQUE_ID= author_unique_id,
            EMAIL= receiver_email,
            STATUS= status,
            PROGRESS= progress,
            PIC= pic,
            REPLY_DONE= is_reply_done,
        ))

        # update slack
        slack.update_post(CHANNEL_ID, MSG_TYPE['BLOCK'], update_msg, slack_thread_id)

        # append data
        updated_data.append({
            'gmail_thread_id': gmail_thread_id,
            'author_unique_id': author_unique_id,
            'slack_thread_id': slack_thread_id,
            'status': status,
            'progress': progress
        })

    return ResType(data=updated_data).get_response()

# result = lambda_handler(None)
# print(result)