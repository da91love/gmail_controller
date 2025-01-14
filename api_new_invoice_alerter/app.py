
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

import pydash as _
from common.AppBase import AppBase
from common.util.get_config import get_config
from api_tiktok_posts_info.type.ResType import ResType
from common.tiktok.get_posts import get_posts
from common.tiktok.get_post_stat import get_post_stat
from common.slack.Slack import Slack
from common.slack.SlackMsgCreator import SlackMsgCreator
from common.const.SLACK import *


# Create instance
config = get_config()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def app_api_new_invoice_alerter(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    data: dict = event
    grouped_by_export_no = _.group_by(data, 'exportNo')

    # declare instance
    slack = Slack()
    for export_no in grouped_by_export_no:
        pi_request_date, export_no = itemgetter('piRequestDate', 'exportNo')(grouped_by_export_no[export_no][0])

        slack_post_msg = SlackMsgCreator.get_slack_new_invoice_post_block(
            shipment_request_date=pi_request_date,
            pi_no=('BSTSPI' + export_no[-11:]),
            export_no=export_no
        )

        res = slack.add_post(
            channel_id=SLACK_GLOBAL_EQB_CHANNEL_ID,
            msg_type=MSG_TYPE['BLOCK'],
            msg_body=slack_post_msg
        )

        thread_ts = res.text

        for export_info in grouped_by_export_no[export_no]:
            productName, productCode, quantity = itemgetter('productName', 'productCode', 'quantity')(export_info)

            slack_reply_msg = SlackMsgCreator.get_slack_new_invoice_details_reply_block(
                productName=productName,
                productCode=productCode,
                quantity=quantity
            )

            slack.add_reply(
                channel_id=SLACK_GLOBAL_EQB_CHANNEL_ID,
                msg_type=MSG_TYPE['BLOCK'],
                msg_body=slack_reply_msg,
                thread_ts=thread_ts
            )

    return ResType(data={}).get_response()