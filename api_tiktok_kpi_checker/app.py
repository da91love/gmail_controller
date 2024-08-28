
# import boto3
import csv
import uuid
from datetime import datetime, timedelta, time
from operator import itemgetter
import pydash as _
from googleapiclient.errors import HttpError
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(api_root)

from common.AppBase import AppBase
from common.util.get_config import get_config
from api_gmail_sender.type.ResType import ResType
from common.lib.ma.data_access.system.AccessService import AccessService
from common.const.DB import *
from common.const.SLACK import *
from common.slack.Slack import Slack
from common.slack.SlackMsgCreator import SlackMsgCreator
from common.util.DateUtil import DateUtil

# Create instance
config = get_config()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def api_tiktok_kpi_checker(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    data = event

    # 금주 컨텐츠 누적
    # Get the current date
    tg_date = datetime.combine(datetime.now(), time.min)
    from_date = DateUtil.get_previous_day(tg_date=tg_date, tg_day='tuesday')
    to_date = tg_date + timedelta(days=1)

    from_date_as_str = from_date.strftime('%Y-%m-%d')
    to_date_as_str = to_date.strftime('%Y-%m-%d')

    posting_history_in_all_t_week = AccessService(GLOBAL).select_posting_history_in_day(from_date=from_date_as_str, to_date=to_date_as_str)

    # sort by created at
    posting_history_in_all_t_week.sort(key=lambda x: x['created_at'], reverse=True)
    uniq_posting_history_in_all_t_week_by_order = _.uniq_by(posting_history_in_all_t_week,'post_id')

    num_of_post_t_week = len(uniq_posting_history_in_all_t_week_by_order)
    sum_play_count_t_week = _.sum_by(uniq_posting_history_in_all_t_week_by_order, 'play_count')

    # 지난주 컨텐츠의 지난주 누적분
    from_date_l_week = from_date - timedelta(days=7)
    to_date_l_week = from_date

    # 지난 주에 포스팅된 포스트만 취득
    posting_history_in_all_l_week = AccessService(GLOBAL).select_posting_history_in_day(from_date=from_date_l_week, to_date=to_date_l_week)

    # 지난주에 올린 포스트의 최근 created 시간으로 필터링
    filtered_posting_history_in_all_l_week = _.filter_(posting_history_in_all_l_week, lambda x: from_date <= x['created_at'] and x['created_at'] < to_date)
    filtered_posting_history_in_all_l_week.sort(key=lambda x: x['created_at'], reverse=True)
    uniq_posting_history_in_all_l_week_by_order = _.uniq_by(filtered_posting_history_in_all_l_week,'post_id')

    # 지난주에 올린 포스트의 저번주까지 누적 조회수 계산
    filtered_posting_history_in_l_week = _.filter_(posting_history_in_all_l_week, lambda x: from_date_l_week <= x['created_at'] and x['created_at'] < to_date_l_week)
    filtered_posting_history_in_l_week.sort(key=lambda x: x['created_at'], reverse=True)
    uniq_posting_history_in_l_week_by_order = _.uniq_by(filtered_posting_history_in_l_week,'post_id')

    num_of_post_l_week = len(uniq_posting_history_in_all_l_week_by_order)
    sum_play_count_l_week = _.sum_by(uniq_posting_history_in_all_l_week_by_order, 'play_count')
    sum_play_count_til_l_week = _.sum_by(uniq_posting_history_in_l_week_by_order, 'play_count')

    sum_play_count_t_week_of_l = sum_play_count_l_week - sum_play_count_til_l_week

    # insert to db
    AccessService(GLOBAL).insert_clm_posting_history(
        tg_date=tg_date,
        this_week_post_num=num_of_post_t_week,
        this_week_view_count=sum_play_count_t_week,
        last_week_post_num=num_of_post_l_week,
        last_week_view_count=sum_play_count_t_week_of_l
    )

    return ResType(data={}).get_response()

result = api_tiktok_kpi_checker(None)
print(result)

