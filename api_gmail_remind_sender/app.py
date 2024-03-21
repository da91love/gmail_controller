
# import boto3
import csv
import uuid
from operator import itemgetter
from datetime import datetime
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
from api_gmail_sender.type.ResType import ResType
from common.gmail.LabelControl import LabelControl

from common.lib.ma.data_access.system.AccessService import AccessService
from api_gmail_remind_sender.const.mail_info import mail_info
from common.const.EMAIL import *
from common.const.STATUS import *

# Create instance
config = get_config()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def app_api_gmail_remind_sender(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    data = event

    # get thread_id
    tg_contacts = AccessService.select_sent_thread_id()
    cnt_num_by_tkey = AccessService.select_contact_num_by_tkey()

    # Group data by threadId
    cnts_grouped_by_tid = _.group_by(tg_contacts, "gmail_thread_id")
    cntc_num_grouped_by_tkey = _.group_by(cnt_num_by_tkey, "t_key")

    # Extract the latest entry for each threadId
    latest_sent_contacts = [_.max_by(group, lambda x: x["created_at"]) for group in cnts_grouped_by_tid.values()]

    remind_mails = []
    remind_mails_num = 0
    for latest_sent_contact in latest_sent_contacts:
        gmail_thread_id, gmail_msg_id, receiver_email, sender_email, t_key, status, progress, pic, created_at \
            = itemgetter('gmail_thread_id', 'gmail_msg_id', 'receiver_email', 'sender_email', 't_key', 'status', 'progress','pic', 'created_at')(latest_sent_contact)

        is_cnt_bf = True if cntc_num_grouped_by_tkey[t_key][0]['thread_count'] > 1 else False
        sent_num = len(cnts_grouped_by_tid[gmail_thread_id])

        # declare instance
        labelControl = LabelControl(sender_email)

        # remind 메일 송신은 300회로 한정
        if remind_mails_num < 150:
            # 이메일 전환으로 이미 보낸 이력이 있을 경우 remind 보내지 않음
            if not is_cnt_bf:
                # only send remind status open
                if status == STATUS['OPEN']:
                    # if sent number is over 5, no remind send
                    if sent_num < 2:
                        # remind if over 5 days # TODO: change days diff
                        day_diff = (datetime.now() - created_at).days
                        if day_diff > 5:
                            # Extract the information you need, e.g., sender, receiver, mail_subject, etc.
                            mail_subject = mail_info[sent_num - 1]['mail_subject']
                            mail_body = mail_info[sent_num - 1]['mail_body']
                            formatted_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                            # Send the message
                            # 이전 스레드가 존재할시 기존 스레드에 엮어서 보내고
                            try:
                                sent_message = send_re_email(sender_email, receiver_email, mail_subject, mail_body, gmail_thread_id)

                                # insert to contact db
                                AccessService.insert_contact_history(
                                    gmail_thread_id=gmail_thread_id,
                                    gmail_msg_id=sent_message.get('id'),
                                    gmail_label_id='SENT',
                                    t_key=t_key,
                                    created_at=formatted_datetime
                                )
                            # 기존 스레드 존재하지 않아 에러 발생 시 새로운 메일로 송신
                            except HttpError as e:
                                sent_message = send_email(sender_email, receiver_email, mail_subject, mail_body)

                                # prepare variables
                                new_gmail_thread_id = sent_message.get("threadId")
                                gmail_msg_id = sent_message.get("id")

                                ## 기존꺼 삭제
                                AccessService.delete_temp_status(old_gmail_thread_id=gmail_thread_id)
                                ## 새로운거 없으면 추가
                                contact_status = AccessService.select_contacts_status(gmail_thread_id=new_gmail_thread_id)
                                if len(contact_status) < 1:
                                    AccessService.insert_contact_status(
                                        gmail_thread_id=new_gmail_thread_id,
                                        status=status,
                                        progress=progress
                                    )

                                # modify label
                                labelControl.add_label(gmail_msg_id=gmail_msg_id, add_label_names=[status, progress, pic])

                                # update contact
                                AccessService.update_gmail_mail_contact_thread_id(
                                    new_gmail_thread_id=new_gmail_thread_id,
                                    old_gmail_thread_id=gmail_thread_id
                                )

                                # insert to contact db
                                AccessService.insert_contact_history(
                                    gmail_thread_id=new_gmail_thread_id,
                                    gmail_msg_id=gmail_msg_id,
                                    gmail_label_id='SENT',
                                    t_key=t_key,
                                    created_at=formatted_datetime
                                )

                            remind_mails.append(sent_message)
                            remind_mails_num += 1

    return ResType(data=remind_mails).get_response()

result = app_api_gmail_remind_sender(None)
print(result)
