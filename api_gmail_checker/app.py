
# import boto3
import csv
import uuid
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(api_root)
import requests

from common.AppBase import AppBase
from common.type.Errors import *
from common.util.get_config import get_config
from common.gmail.check_emails import check_emails
from api_gmail_sender.type.ResType import ResType
from common.const.API_URL import SLACK_URL

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
    mail_check_res = check_emails(label_id)

    # create slack thread
    for res in mail_check_res:
        body = {
            'type': 'block',
            'channel': 'C068UMGLCDQ',
            'msg': 'testtesttest'
        }
        slack_res = requests.post(SLACK_URL, body)

        print(slack_res)

    return ResType(data=res).get_response()

# labelId = sys.argv[1]
#
# result = lambda_handler({
#     "label_id": labelId,
# })
#
# print(result)