
# import boto3
import csv
import uuid
import os
import sys
from mysql.connector.errors import *
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
from common.lib.ma.data_access.system.AccessService import AccessService

# Create instance
config = get_config()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def app_api_gmail_checker(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    data = event
    label_id = data.get('labelId')

    if any(value is None for value in [label_id]):
        raise IrrelevantParamException

    # check new mails
    mail_check_res = check_emails(label_id)

    db_inserted_res = []
    for res in mail_check_res:
        try:
            # insert to contact db
            AccessService.insert_contact_history(
                gmail_thread_id=res['gmail_thread_id'],
                gmail_msg_id=res['gmail_msg_id'],
                gmail_label_id=res['gmail_label_id'],
                author_unique_id=res['author_unique_id'],
                seeding_num=res['seeding_num'],
                tg_brand=res['tg_brand'],
                created_at=res['created_at']
            )

            AccessService.insert_contents(
                gmail_thread_id=res['gmail_thread_id'],
                gmail_msg_id=res['gmail_msg_id'],
                contents=res['contents'],
                created_at=res['created_at']
            )

            # create slack thread
            slack_wrapper(res)

            # put into list
            db_inserted_res.append(res)

        # 데이터베이스 primary key 중복 오류
        except IntegrityError:
            pass

    return ResType(data=db_inserted_res).get_response()

# labelId = sys.argv[1]
#
# result = app_api_gmail_checker({
#     "labelId": labelId,
# })
#
# print(result)

