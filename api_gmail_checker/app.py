
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
from common.gmail.check_emails import check_emails
from api_gmail_sender.type.ResType import ResType

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
    res = check_emails(label_id)

    # create slack thread


    return ResType(data=res).get_response()

labelId = sys.argv[1]

result = lambda_handler({
    "label_id": labelId,
})

print(result)