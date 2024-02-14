
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
from common.type.Errors import *
from common.util.get_config import get_config
from common.gmail.send_re_email import send_re_email
from common.gmail.send_email import send_email
from common.gmail.update_gmail_thread_id import update_gmail_thread_id
from common.slack.slack_wrapper import slack_wrapper
from api_gmail_follow_up_sender.type.ResType import ResType
from api_gmail_follow_up_sender.const.mail_info import *
from common.const.EMAIL import *
from common.const.STATUS import *

from common.lib.ma.data_access.system.AccessService import AccessService

# Create instance
config = get_config()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def app_api_gmail_follow_up_sender(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # post master db에 포함된 인원 추출
    # eoeo이나 피키는 쿼리에서 필터링
    data = event
    tg_infls = AccessService.select_follow_up_tg_list()

    # for loop로 위에서 추출된 인원 중 mail_contents에 follow-up메일 송신한 적 없는 사람 추출
    sent_done_tg = []
    for tg_infl in tg_infls:
        t_key, tiktok_url, posted_time = itemgetter('t_key', 'tiktok_url', 'posted_time')(tg_infl)

        # follow up 유무로 필터링
        is_follow_up_done = AccessService.select_follow_up_by_thread(t_key=t_key)
        if not is_follow_up_done:

            # post 업로드 3일 후 메일
            day_diff = (datetime.now() - (posted_time or datetime.now())).days
            if day_diff > 3:
                # t_key로 메일 스레드 추출
                # follow_up_mail_info가 1보다 작으면 eoeo이나 picky에서 온 인원들로 메일주소 자체가 없어 메일 송신하지 않음
                follow_up_mail_info = AccessService.select_follow_up_mail_info_by_tkey(t_key=t_key)
                gmail_thread_id, receiver_email = itemgetter('gmail_thread_id', 'receiver_email')(follow_up_mail_info[0])

                # create mail body
                formatted_mail_body = mail_body.format(tiktok_url)

                # 메일 송신
                sent_message = None
                try:
                    sent_message = send_re_email(SENDER_EMAIL, receiver_email, mail_subject, formatted_mail_body, gmail_thread_id)
                except HttpError:
                    sent_message = send_email(SENDER_EMAIL, receiver_email, mail_subject, formatted_mail_body)

                    # prepare variables
                    new_gmail_thread_id = sent_message.get("threadId")

                    # update database
                    update_gmail_thread_id(
                        new_gmail_thread_id= new_gmail_thread_id,
                        old_gmail_thread_id= gmail_thread_id
                    )

                finally:
                    # create params
                    redefined_gmail_thread_id = sent_message.get("threadId")
                    formatted_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    gmail_msg_id = sent_message.get('id')
                    gmail_label_id = 'SENT'

                    # insert to follow up check db
                    AccessService.insert_follow_up_check(t_key=t_key)

                    # insert to contact db
                    AccessService.insert_contact_history(
                        gmail_thread_id=redefined_gmail_thread_id,
                        gmail_msg_id=gmail_msg_id,
                        gmail_label_id=gmail_label_id,
                        t_key=t_key,
                        created_at=formatted_datetime
                    )

                    slack_params = {
                        'gmail_thread_id': redefined_gmail_thread_id,
                        'gmail_msg_id': gmail_msg_id,
                        'gmail_label_id': gmail_label_id,
                        'created_at': formatted_datetime,
                        't_key': t_key,
                        'contents': formatted_mail_body,
                    }

                    # create slack thread
                    slack_wrapper(slack_params)

                    sent_done_tg.append(sent_message)

    return ResType(data=sent_done_tg).get_response()

# result = app_api_gmail_follow_up_sender(None)
# print(result)

