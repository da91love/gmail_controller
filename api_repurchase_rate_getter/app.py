
# import boto3
import csv
import uuid
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import pydash as _
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(api_root)

from common.AppBase import AppBase
from common.util.get_config import get_config
from api_tiktok_posts_info.type.ResType import ResType
from common.tiktok.get_posts import get_posts
from common.lib.ma.data_access.system.AccessService import AccessService
from common.const.DB import *
from common.util.FsUtil import *

# Create instance
config = get_config()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def app_api_repurchase_rate_getter(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    # data = event
    # start_date: str = data.get('uniqId')
    # end_date: int = data.get('period')

    tg_period = 24
    start_date = '2024-02-01'
    end_date = '2024-09-02'

    # calculate month diff
    # Define the two dates
    date1 = datetime.strptime(end_date, "%Y-%m-%d")
    date2 = datetime.strptime(start_date, "%Y-%m-%d")

    # Calculate the difference in months
    month_diff = (date1.year - date2.year) * 12 + (date1.month - date2.month)

    all_orders = AccessService(BOOSTERS).select_all_orders(
        start_date=start_date,
        end_date=end_date
    )

    # get amazon order id with buyer name data
    amz_buyer_names = FsUtil.open_json_2_json_file(project_root + "/common/public/input/amz_order_cstm_name.json")

    # create id
    order_with_id = {}
    if len(all_orders) > 0:
        for order in all_orders:
            addr_json = json.loads(order.get('address_json'))
            amz_order_id = order.get('amazon_order_id')

            # create primary key
            name = amz_buyer_names.get(amz_order_id) or 'None'
            country = addr_json.get('Country') or 'None'
            state = addr_json.get('State') or 'None'
            city = addr_json.get('City') or 'None'
            postal_code = addr_json.get('PostalCode') or 'None'

            id = f'{name}_{country}_{state}_{city}_{postal_code}'

            date_obj = order.get('real_purchase_date')
            date_as_yyyymm = date_obj.strftime("%Y") + date_obj.strftime("%m")

            if order_with_id.get(id):
                (order_with_id[id]).append(date_as_yyyymm)
            else:
                order_with_id[id] = [date_as_yyyymm]


    #
    date_clct = {}
    for i in range(0, month_diff+1):
        # Convert string to datetime object
        date_obj = datetime.strptime(start_date, "%Y-%m-%d")

        # Add one month using relativedelta
        tg_date_obj = date_obj + relativedelta(months=i)
        tg_date_as_yyyymm = tg_date_obj.strftime("%Y") + tg_date_obj.strftime("%m")

        # add tg date
        date_clct[tg_date_as_yyyymm] = None

        # filter ids which has target date
        ids_including_prd = {}
        for id in order_with_id:
            if tg_date_as_yyyymm in order_with_id[id]:
                ids_including_prd[id] = order_with_id[id]

        # prepare variable
        m_d_clct = {}

        # insert unique num of buyer
        m_d_clct['init_sales'] = len(ids_including_prd)
        for j in range(0, month_diff-i+1):
            # Add one month using relativedelta
            tg_j_date_obj = tg_date_obj + relativedelta(months=j)
            tg_j_date_as_yyyymm = tg_j_date_obj.strftime("%Y") + tg_j_date_obj.strftime("%m")

            sum_by_period = 0
            for id in ids_including_prd:
                prd_list_by_id = ids_including_prd[id]

                count = prd_list_by_id.count(tg_j_date_as_yyyymm)

                sum_by_period += count

            d_name = f'M+{j}'

            m_d_clct[d_name] = sum_by_period

        # 본데이터에서 한번 타겟한 id 모두 삭제
        for id in ids_including_prd:
            del order_with_id[id]

        # M+0 수 조정
        m_d_clct['M+0'] = m_d_clct['M+0'] - m_d_clct['init_sales']

        # 데이터 갈아끼우기
        date_clct[tg_date_as_yyyymm] = m_d_clct

    return ResType(data=date_clct).get_response()