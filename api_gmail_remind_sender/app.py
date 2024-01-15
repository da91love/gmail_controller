
# import boto3
import csv
import uuid
from operator import itemgetter
from datetime import datetime
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
from common.gmail.send_remind_email import send_remind_email
from api_gmail_sender.type.ResType import ResType

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

    # Group data by threadId
    grouped_data = _.group_by(tg_contacts, "gmail_thread_id")

    # Extract the latest entry for each threadId
    latest_sent_contacts = [_.max_by(group, lambda x: x["created_at"]) for group in grouped_data.values()]

    re_sent_mails = []
    for latest_sent_contact in latest_sent_contacts:
        gmail_thread_id, gmail_msg_id, receiver_email, t_key, status, created_at \
            = itemgetter('gmail_thread_id', 'gmail_msg_id', 'receiver_email', 't_key', 'status', 'created_at')(latest_sent_contact)

        sent_num = len(grouped_data[gmail_thread_id])

        # only send remind status open
        if status == STATUS['OPEN']:
            # if sent number is over 5, no remind send
            if sent_num < 4:
                # remind if over 5 days # TODO: change days diff
                if (datetime.now() - created_at).days >= 3:
                    # Extract the information you need, e.g., sender, receiver, mail_subject, etc.
                    mail_subject = mail_info[sent_num - 1]['mail_subject']
                    mail_body = mail_info[sent_num - 1]['mail_body']
                    formatted_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # Send the message
                    sent_message = send_remind_email(SENDER_EMAIL, receiver_email, mail_subject, mail_body, gmail_thread_id)

                    # insert to contact db
                    AccessService.insert_contact_history(
                        gmail_thread_id=gmail_thread_id,
                        gmail_msg_id=sent_message.get('id'),
                        gmail_label_id='SENT',
                        t_key=t_key,
                        created_at=formatted_datetime
                    )

                    re_sent_mails.append(sent_message)

    return ResType(data=re_sent_mails).get_response()

result = app_api_gmail_remind_sender(None)
print(result)
