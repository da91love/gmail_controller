
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

from api_gmail_checker.type.ResType import ResType
from common.AppBase import AppBase
from common.type.Errors import *
from common.util.get_config import get_config
from common.util.logger_get import get_logger
from common.scm.amazon.Amazon import Amazon
from common.scm.rincos.Rincos import Rincos
from common.lib.ma.data_access.system.AccessService import AccessService

# Create instance
config = get_config()
logger = get_logger()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def app_api_delivery_tracker(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    eventdata = event

    tracking_tg_invoices = AccessService.select_delivery_info()

    # declare instances
    rincos = Rincos()
    amazon = Amazon()

    result = []
    for invoices in tracking_tg_invoices:
        courier = invoices['courier']
        order_id = invoices['order_id']
        invoice_id = invoices['invoice_id']

        # select delivery history
        delivery_history = AccessService.select_delivery_history(invoice_id=invoice_id)

        data = []
        if courier == 'RINCOS':
            res = rincos.get_tracking_details(invoice_id=invoice_id)
            history = res['result']

            data = rincos.convert_2_bsts_db(history)

        elif courier == 'AMAZON':
            res = amazon.get_tracking_details(invoice_id=invoice_id)
            history = res['payload']['eventHistory']

            data = amazon.convert_2_bsts_db(history)

        if len(delivery_history) < len(data):
            # insert to data into delivery history tb
            for d in data:
                try:
                    AccessService.insert_delivery_history(
                        order_id=order_id,
                        invoice_id=invoice_id,
                        delivery_status=d['delivery_status'],
                        event_time=d['event_time']
                    )
                except IntegrityError as e:
                    logger.error(e)
                    continue

            # update data in delivery master
            AccessService.update_delivery_master(
                order_id=order_id,
                invoice_id=invoice_id,
                delivery_status=data[-1]['delivery_status'],
            )

            # append to result
            result.append(invoice_id)

    return ResType(data=result).get_response()

# labelId = sys.argv[1]
#
# result = app_api_gmail_checker({
#     "labelId": labelId,
# })
#
# print(result)

