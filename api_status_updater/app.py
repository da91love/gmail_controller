
# import boto3
import csv
import json
from operator import itemgetter
import os
import sys
from mysql.connector.errors import *
from googleapiclient.errors import HttpError
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
from common.gmail.LabelControl import LabelControl
from common.gmail.check_label import check_label
from common.lib.ma.data_access.system.AccessService import AccessService

# Create instance
config = get_config()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def app_api_status_updater(event, context=None):
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
    labelControl = LabelControl()

    # 20분이내 업데이트된 status 데이터 취득
    status_data = AccessService.select_status_in_x_min()

    updated_data = []
    if len(status_data) > 0:

        # update slack
        for sd in status_data:
            status, progress = itemgetter('status', 'progress')(sd)
            gmail_thread_id = sd['gmail_thread_id']

            # gmail 및 slack 공통 데이터 미리 취득
            contact_data = AccessService.select_contacts(gmail_thread_id=gmail_thread_id)
            gmail_msg_id, t_key = itemgetter('gmail_msg_id', 't_key')(contact_data[0])

            slack_need_info = AccessService.select_slack_need_info(t_key=t_key)[0]
            author_unique_id, receiver_email, tiktok_url, pic = itemgetter('author_unique_id', 'receiver_email', 'tiktok_url', 'pic')(slack_need_info)

            # 아직 답장이 안온 경우는 Slack 존재하지 않으므로 pass
            slack_id_info = AccessService.select_slack_thread_history(gmail_thread_id=gmail_thread_id)
            if len(slack_id_info) > 0:
                slack_thread_id = itemgetter('slack_thread_id')(slack_id_info[0])

                is_reply_done = True if contact_data[-1]['gmail_label_id'] == 'SENT' else False

                # Modify slack status
                update_msg = SlackMsgCreator.get_slack_post_block(
                    tiktok_url= tiktok_url,
                    author_unique_id= author_unique_id,
                    receiver_email= receiver_email,
                    status= status,
                    progress= progress,
                    pic= pic,
                    is_reply_done= is_reply_done,
                )

                # update slack
                slack.update_post(CHANNEL_ID, MSG_TYPE['BLOCK'], update_msg, slack_thread_id)

            # update gmail label
            # 이미 삭제된 메일에 대해 label 변경 처리시 에러처리
            try:
                mail_labels = check_label(gmail_msg_id=gmail_msg_id)
                labelControl.remove_label(gmail_msg_id=gmail_msg_id,remove_label_ids=mail_labels)
                labelControl.add_label(gmail_msg_id=gmail_msg_id, add_label_names=[status, progress, pic])
            except HttpError as e:
                pass

            # append data
            updated_data.append({
                'gmail_thread_id': gmail_thread_id
            })

    return ResType(data=updated_data).get_response()

# result = app_api_status_updater(None)
# print(result)