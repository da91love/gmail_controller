
# import boto3
import csv
import uuid
import traceback
from datetime import datetime
from operator import itemgetter
import pydash as _
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(api_root)

from common.AppBase import AppBase
from common.type.Errors import *
from common.util.get_config import get_config
from common.util.logger_get import get_logger
from common.slack.Slack import Slack
from common.slack.SlackMsgCreator import SlackMsgCreator
from api_gmail_sender.type.ResType import ResType
from common.const.EMAIL import *
from common.const.SLACK import *
from common.lib.ma.data_access.system.AccessService import AccessService

# Create instance
config = get_config()
logger = get_logger()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def app_api_mia_reminder(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    data = event
    tgs_mia = AccessService.select_mia()
    grouped_tgs_mia = _.group_by(tgs_mia, 't_key')

    # declare instance
    slack = Slack()

    tg_remind_mia = []
    for t_key in grouped_tgs_mia:
        tg_mia = grouped_tgs_mia[t_key]

        label_ids = [tg['gmail_label_id'] for tg in tg_mia]

        # 한번이라도 답장 온 타겟
        if INBOX in label_ids:
            # 마지막 label SENT
            last_contact_tg_mia = tg_mia[-1]

            gmail_thread_id, author_unique_id, gmail_label_id, receiver_email, sender_email, pic, status, progress, tiktok_url, created_at \
                = itemgetter('gmail_thread_id', 'author_unique_id', 'gmail_label_id', 'receiver_email', 'sender_email', 'pic', 'status', 'progress', 'tiktok_url', 'created_at')(last_contact_tg_mia)

            # if gmail_label_id == SENT:

            # 마지막 contact에서 3일 이상 지난 mia
            day_diff = (datetime.now() - created_at).days
            if day_diff > 3:
                post_msg = SlackMsgCreator.get_slack_remind_post_block(
                    tiktok_url=tiktok_url,
                    gmail_label_id=gmail_label_id,
                    author_unique_id=author_unique_id,
                    receiver_email=receiver_email,
                    sender_email=sender_email,
                    pic=pic,
                    status=status,
                    progress=progress,
                    created_at=created_at
                )
                slack_res = slack.add_post(SLACK_REMIND_CHANNEL_ID, MSG_TYPE['BLOCK'], post_msg)

                try:
                    if slack_res.status_code == 200:
                        tg_remind_mia.append({
                            't_key': t_key,
                            'gmail_thread_id': gmail_thread_id,
                            'author_unique_id': author_unique_id,
                            'receiver_email': receiver_email
                        })
                    else:
                        raise SlackApiInternalException(msg=slack_res.text)
                except SlackApiInternalException:
                    logger.error(traceback.format_exc())
                    pass

    return ResType(data=tg_remind_mia).get_response()

# result = app_api_mia_reminder(None)
# print(result)

