
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

from Packing import Packing

from common.tiktok.get_post_stat import get_post_stat
from common.slack.Slack import Slack
from common.slack.SlackMsgCreator import SlackMsgCreator
from common.const.SLACK import *


# Create instance
config = get_config()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def app_api_packing_calculator(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    data: dict = event

    # declare instance
    packing = Packing()


    packing.calculate_box_packing(data)

    boxes_info = packing.boxes_info
    boxes_info_by_box_type = []
    for item_code in boxes_info:
        boxes_gby_box_name = _.group_by(boxes_info[item_code], 'box_name')
        for box_name in boxes_gby_box_name:
            boxes_info_by_box_type.append({
                "id": item_code,
                "box_type": box_name,
                "group": item_code,
                "q": len(boxes_gby_box_name[box_name]),
                "w": boxes_gby_box_name[box_name][0]['width'],
                "d": boxes_gby_box_name[box_name][0]['length'],
                "h": boxes_gby_box_name[box_name][0]['height'],
                "wg": boxes_gby_box_name[box_name][0]['gross_weight'],
                "vr": 0,
            })

    packing.caculate_pallet_packing(boxes_info_by_box_type)
    res = {
        'packing_smr': packing.packing_smr,
        'pallet_packing': packing.pallet_packing,

    }

    return ResType(data=res).get_response()