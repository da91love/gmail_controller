
# import boto3
import csv
import uuid
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
from common.gmail.send_email import send_email
from common.gmail.LabelControl import LabelControl
from api_gmail_sender.type.ResType import ResType
from api_gmail_sender.const.mail_info import *
from common.const.EMAIL import *
from common.const.STATUS import *

from common.lib.ma.data_access.system.AccessService import AccessService

# Create instance
config = get_config()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def app_api_gmail_converting_sender(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    data = event
    # 과거에 답장온 회수가 1회 이상이고, status가 open인 대상에게 메일 변경 안내 메일 송신
    tg_infls = AccessService.select_past_on_contact_infl(tg_date='2024-01-23')
    old_thread_id_by_tkey = _.group_by(AccessService.select_latest_thread_id_by_tkey(), "t_key")

    # declare instance
    labelControl = LabelControl()

    sent_done_tg = []
    for tg_infl in tg_infls:

        # modify label, if pic is not registered process end
        t_key, author_unique_id, receiver_email, pic = itemgetter('t_key', 'author_unique_id', 'receiver_email', 'pic')(tg_infl)

        # send mail
        # format mail body
        formatted_mail_body = mail_body.format(author_unique_id)

        # send gmail
        sent_message = send_email(
            sender_email=SENDER_EMAIL,
            receiver_email=receiver_email,
            mail_subject=mail_subject,
            mail_body=formatted_mail_body,
        )

        # prepare variables
        gmail_thread_id = sent_message.get("threadId")
        gmail_msg_id = sent_message.get("id")
        formatted_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # get old t_key
        old_gmail_thread_id = old_thread_id_by_tkey[t_key][0]['gmail_thread_id']

        # status
        ## 기존꺼 삭제
        AccessService.delete_temp_status(old_gmail_thread_id=old_gmail_thread_id)
        ## 새로운거 없으면 추가
        contact_status = AccessService.select_contacts_status(gmail_thread_id=gmail_thread_id)
        if len(contact_status) < 1:
            AccessService.insert_contact_status(
                gmail_thread_id=gmail_thread_id,
                status='open',
                progress='negotiating'
            )

        # update slack
        AccessService.update_slack_thread_id(
            new_gmail_thread_id=gmail_thread_id,
            old_gmail_thread_id=old_gmail_thread_id
        )

        # update mail contents
        AccessService.update_gmail_mail_contents_thread_id(
            new_gmail_thread_id=gmail_thread_id,
            old_gmail_thread_id=old_gmail_thread_id
        )

        # update mail contact
        AccessService.update_gmail_mail_contact_thread_id(
            new_gmail_thread_id=gmail_thread_id,
            old_gmail_thread_id=old_gmail_thread_id
        )

        # modify label
        labelControl.add_label(
            gmail_msg_id=gmail_msg_id,
            add_label_names=[STATUS['OPEN'], PROGRESS['NEGOTIATING'], pic]
        )

        # insert to contact db
        AccessService.insert_contact_history(
            gmail_thread_id=gmail_thread_id,
            gmail_msg_id=gmail_msg_id,
            gmail_label_id='SENT',
            t_key=t_key,
            created_at=formatted_datetime
        )

        # append result
        sent_done_tg.append(sent_message)

    return ResType(data=sent_done_tg).get_response()

# result = app_api_gmail_sender(None)
# print(result)

