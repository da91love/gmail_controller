
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
import requests
from const.AUTH import *
from const.API import *
from const.PACKING_SPEC import *
from const.VISUAL_CONF import *

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

    box_d = []
    leftBoxes = []
    # 팔레트의 최대 수량으로 나누어 나머지 박스들 리스트에 적재
    for box_info in data:
        item_code = box_info['group']
        max_box_d_in_pallet = MAX_BOX_D_IN_pallet[item_code]
        box_q = box_info['q']

        if (box_q / max_box_d_in_pallet) > 1 and 'BOX_D' in box_info['id']:
            box_info['q'] = box_q - (box_q % max_box_d_in_pallet)

            copied_box_info = _.clone_deep(box_info)
            copied_box_info['q'] = box_q % max_box_d_in_pallet
            del copied_box_info['group']

            box_d.append(box_info)
            leftBoxes.append(copied_box_info)
        else:
            del box_info['group']
            leftBoxes.append(box_info)


    all_calc_target_boxes = [box_d, leftBoxes]

    bins_packed = []
    for tg_box in all_calc_target_boxes:
        req = {
            "username": USER_NAME,
            "api_key": API_KEY,
            "bins": pallet_SPEC,
            "items": tg_box,
            "params": VISUAL_CONF
        }

        res = requests.post(BIN_PACKING_API_URL, json=req)

        if res.status_code == 200:
            json_res = res.json()

            for bin_packed in json_res['response']['bins_packed']:
                bins_packed.append(bin_packed)

        elif res.status_code == 401:
            raise Exception

    bins_packed_smr = []
    for bin_packed in bins_packed:
        bins_packed_smr.append({
            'stack_width': 1.1,
            'stack_length': 1.1,
            'stack_height': bin_packed['bin_date']['stack_height'] + 0.13,
            'image_complete': bin_packed['image_complete'],
            'cartons': len(bin_packed['items'])
        })

    print('1')

    return ResType(data={}).get_response()