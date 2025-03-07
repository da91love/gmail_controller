
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

    buyer_name = data.get('buyer_name')
    input = data.get('data')

    # declare instance
    packing = Packing(buyer_name=buyer_name)

    # calculate box packing
    packing.calculate_box_packing(input)

    # set summary
    packing.set_box_packing_summary()

    boxes_info_by_box_type = []
    boxes_gby_group = _.group_by(packing.boxes_info, 'group')
    for group in boxes_gby_group:
        boxes_gby_box_name = _.group_by(boxes_gby_group[group], 'box_name')
        for box_name in boxes_gby_box_name:
            boxes_info_by_box_type.append({
                "id": group,
                "box_type": box_name,
                "group": group,
                "q": len(boxes_gby_box_name[box_name]),
                "w": boxes_gby_box_name[box_name][0]['width'],
                "d": boxes_gby_box_name[box_name][0]['length'],
                "h": boxes_gby_box_name[box_name][0]['height'],
                "wg": boxes_gby_box_name[box_name][0]['gross_weight'],
                "vr": 0,
            })

    # calculate pallet packing
    packing.calculate_pallet_packing(boxes_info_by_box_type)

    # set pallet packing
    packing.set_pallet_packing_smr()

    # set pallet detail packing
    packing.set_pallet_packing_details_smr()

    res = {
        'box_packing_smr': packing.box_packing_smr,
        'pallet_packing_smr': packing.pallet_packing_smr,
        'pallet_packing_detail_smr': packing.pallet_packing_detail_smr
    }

    return ResType(data=res).get_response()