
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
from common.gmail.send_email import send_email
from api_gmail_sender.type.ResType import ResType
from api_gmail_sender.const.mail_info import *

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

    sender_email = data.get('sender_email')
    receiver_email = data.get('receiver_email')
    author_unique_id = data.get('author_unique_id')
    tiktok_url = data.get('tiktok_url')

    if any(value is None for value in [sender_email, receiver_email, author_unique_id, tiktok_url]):
        raise IrrelevantParamException

    # format mail body
    formatted_mail_body = mail_body.format(author_unique_id)

    res = send_email(
        sender_email=sender_email,
        receiver_email=receiver_email,
        mail_subject=mail_subject,
        mail_body=formatted_mail_body,
        author_unique_id=author_unique_id,
        tiktok_url=tiktok_url
    )

    return ResType(data=res).get_response()

sender_email = sys.argv[1]
receiver_email = sys.argv[2]
author_unique_id = sys.argv[3]
tiktok_url = sys.argv[4]

result = lambda_handler({
    "sender_email": sender_email,
    "receiver_email": receiver_email,
    "author_unique_id": author_unique_id,
    "tiktok_url": tiktok_url,
})

print(result)