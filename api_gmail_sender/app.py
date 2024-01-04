
# import boto3
import csv
import uuid
from datetime import datetime
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
def app_api_gmail_sender(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    data = event

    author_unique_id = data.get('authorUniqueId')
    seeding_num = data.get('seedingNum')
    tg_brand = data.get('tgBrand')
    receiver_email = data.get('receiverEmail')

    # declare instance
    labelControl = LabelControl()

    if any(value is None for value in [author_unique_id, seeding_num, tg_brand, receiver_email]):
        raise IrrelevantParamException

    # modify label, if pic is not registered process end
    pic = (AccessService.select_pic(author_unique_id=author_unique_id, seeding_num=seeding_num, tg_brand=tg_brand)[0])['pic']

    # send mail
    # format mail body
    formatted_mail_body = mail_body.format(author_unique_id)

    # send gmail
    sent_message = send_email(
        sender_email= sender_email,
        receiver_email=receiver_email,
        mail_subject=mail_subject,
        mail_body=formatted_mail_body,
    )

    # prepare variables
    gmail_thread_id = sent_message.get("threadId")
    gmail_msg_id = sent_message.get("id")
    formatted_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # modify label
    labelControl.add_label(gmail_msg_id=gmail_msg_id, add_label_names=[status['OPEN'], progress['NEGOTIATING'], pic])

    # insert to contact db
    AccessService.insert_contact_history(
        gmail_thread_id=gmail_thread_id,
        gmail_msg_id=gmail_msg_id,
        gmail_label_id='SENT',
        author_unique_id=author_unique_id,
        seeding_num=seeding_num,
        tg_brand=tg_brand,
        created_at=formatted_datetime
    )

    # insert to status db
    AccessService.insert_contact_status(
        gmail_thread_id=gmail_thread_id,
        status=status['OPEN'],
        progress=progress['NEGOTIATING'],
    )

    return ResType(data=sent_message).get_response()

authorUniqueId = sys.argv[1]
seedingNum = sys.argv[2]
tgBrand = sys.argv[3]
receiverEmail = sys.argv[4]

result = app_api_gmail_sender({
    "authorUniqueId": authorUniqueId,
    "seedingNum": seedingNum,
    "tgBrand": tgBrand,
    "receiverEmail": receiverEmail,
})

print(result)