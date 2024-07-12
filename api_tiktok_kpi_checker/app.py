
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
    pic_email_matches = AccessService.select_pic_email_match()

    # 연락횟수 count
    cnct_num_sum = 0
    today = datetime.now().strftime('%Y-%m-%d')
    for pic_email_match in pic_email_matches:
        sender_email = pic_email_match['sender_email']

        contacts_by_sender_email = AccessService.select_today_contacts(
            today=today,
            sender_email=sender_email
        )

        cnct_num_sum += len(contacts_by_sender_email)

    # 계약횟수 count
    delivery_num = len(AccessService.select_delivery_info_master(today=today))

    # 새로보낸 메일수
    today_contact_num = len(AccessService.select_sent_mail_contact(today=today))

    # 앞으로 보낼 메일수
    future_contact_num = len(AccessService.select_infl_first_contact())

    # 오늘 올린 포스트수
    posts_info = AccessService.select_today_post(today=today)
    post_count = len(posts_info)
    post_url = ', '.join([post_info['tiktok_url'] for post_info in posts_info])

    # 금주 컨텐츠 누적
    # Get the current date
    today_as_min = datetime.combine(datetime.now(), time.min)
    to_date = today_as_min + timedelta(days=1)
    from_date = DateUtil.get_previous_day(tg_date=today_as_min, tg_day='monday')

    to_date_as_str = to_date.strftime('%Y-%m-%d')
    from_dateas_str = from_date.strftime('%Y-%m-%d')

    posting_history_in_all_t_week = AccessService.select_posting_history_in_day(from_date=from_dateas_str, to_date=to_date_as_str)

    # sort by created at
    posting_history_in_all_t_week.sort(key=lambda x: x['created_at'], reverse=True)
    uniq_posting_history_in_all_t_week_by_order = _.uniq_by(posting_history_in_all_t_week,'post_id')

    num_of_post_t_week = len(uniq_posting_history_in_all_t_week_by_order)
    sum_play_count_t_week = _.sum_by(uniq_posting_history_in_all_t_week_by_order, 'play_count')

    # 지난주 컨텐츠의 지난주 누적분
    to_date_l_week = from_date
    from_date_l_week = from_date - timedelta(days=7)

    # 지난 주에 포스팅된 포스트만 취득
    posting_history_in_all_l_week = AccessService.select_posting_history_in_day(from_date=from_date_l_week, to_date=to_date_l_week)

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

    # insert to db
    AccessService.insert_clm_posting_history(
        this_week_post_num=num_of_post_t_week,
        this_week_view_count=sum_play_count_t_week,
        last_week_post_num=num_of_post_l_week,
        last_week_view_count=sum_play_count_l_week - sum_play_count_til_l_week
    )

    # create slack msg
    post_msg = SlackMsgCreator.get_slack_tiktok_kpi_post_block(
        today=today,
        today_contact_count=today_contact_num,
        future_contact_count=future_contact_num,
        cnct_count=cnct_num_sum,
        delivery_count=delivery_num,
        post_count=post_count,
        post_url=post_url,
        this_week_posts=num_of_post_t_week,
        this_week_play_count=sum_play_count_t_week,
        last_week_posts=num_of_post_l_week,
        last_week_play_count=sum_play_count_l_week - sum_play_count_til_l_week,
    )

    # declare instance
    slack = Slack()

    slack.add_post(SLACK_GLOBAL_SEEDING_CHANNEL_ID, MSG_TYPE['BLOCK'], post_msg)


    return ResType(data={}).get_response()

# result = app_api_kpi_checker(None)
# print(result)

