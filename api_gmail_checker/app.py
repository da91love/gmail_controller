
# import boto3
import csv
import uuid
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(api_root)

from common.AppBase import AppBase
from common.type.Errors import *
from common.util.get_config import get_config
from api_gmail_checker.type.ResType import ResType
from common.gmail.check_emails import check_emails
from common.slack.slack_wrapper import slack_wrapper

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
    label_id = data.get('label_id')

    if any(value is None for value in [label_id]):
        raise IrrelevantParamException

    # check new mails
    # mail_check_res = check_emails(label_id)
    mail_check_res = [{'gmail_thread_id': '18c8168754f5ecf9', 'gmail_msg_id': '18c8168be511c5a2', 'gmail_label_id': 'INBOX', 'sender_email': 'eqqualberry.comm@boosters.kr', 'receiver_email': 'daseul.kim@boosters.kr', 'contents': 'bdfbdgdgd 2023년 12월 19일 (화) 오후 6:29, &lt;eqqualberry.comm@boosters.kr&gt;님이 작성: Hi daseul.kim, I hope this message finds you well😀 My name is Anna, and I represent Eqqualberry, a Korean Skincare brand', 'create_at': '2023-12-19 18:29:23'}]

    # create slack thread
    for res in mail_check_res:
        slack_wrapper(res)

    return ResType(data=res).get_response()

# labelId = sys.argv[1]
#
# result = lambda_handler({
#     "label_id": labelId,
# })
#
# print(result)