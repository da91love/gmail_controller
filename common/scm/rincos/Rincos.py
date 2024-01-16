import requests
from datetime import datetime

from common.const.STATUS import EMS_DELIVERY_STATUS
from common.util.get_config import get_config

config = get_config()
class Rincos:
    def __init__(self, ):
        pass

    def get_tracking_details(self, invoice_id):
        try:

            api_url = 'http://www.rincosmall.com/api/order/TrackSendReq.do'
            params = {
             'barcode': invoice_id
            }

            res = requests.get(api_url, params=params)

            if res.status_code == 200:
                res_json = res.json()
                return res_json

        except Exception as e:
            raise e

    def convert_2_bsts_db(self, tracking_details: list):
        try:

            histories = []
            for tracking_detail in tracking_details:
                rincos_status = tracking_detail['status']
                delivery_status = EMS_DELIVERY_STATUS[rincos_status]

                scan_date = tracking_detail['scan_date']
                scan_time = tracking_detail['scan_time']

                # Concatenate the date and time strings
                datetime_str = scan_date + " " + scan_time

                # Parse the concatenated string into a datetime object
                event_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

                histories.append({
                    'delivery_status': delivery_status,
                    'event_time': event_time
                })

            return histories
        except Exception as e:
            raise e
