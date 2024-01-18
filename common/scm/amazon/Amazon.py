
import requests
from datetime import datetime

from common.type.Errors import AmzApiAuthenticationException
from common.const.API_URL import *
from common.util.get_config import get_config

config = get_config()
class Amazon:
    def __init__(self, ):
        self.lwa_api_token = self.__get_lwa_api_token()
        self.rdt_api_token = self.__get_rdt_api_token(
                lwa_api_token=self.lwa_api_token,
                method='GET',
                path='/shipping/v1/tracking/{trackingId}'
            )

    def get_tracking_details(self, invoice_id: str):
        try:
            headers = {
                'x-amz-access-token': self.rdt_api_token
            }

            api_url = f'https://sellingpartnerapi-na.amazon.com/shipping/v1/tracking/{invoice_id}'

            res = requests.get(api_url, headers=headers)

            if res.status_code == 200:
                res_json = res.json()
                payload = (res_json.get('payload')).get('eventHistory')

                return payload

        except Exception as e:
            raise e
    def convert_2_bsts_db(self, tracking_details: list):
        try:

            histories = []
            for tracking_detail in tracking_details:
                delivery_status = tracking_detail['eventCode']
                event_time = datetime.strptime(tracking_detail['eventTime'], "%Y-%m-%dT%H:%M:%SZ")

                histories.append({
                    'delivery_status': delivery_status,
                    'event_time': event_time
                })

            return histories
        except Exception as e:
            raise e

    def __get_lwa_api_token(self):
        try:
            res = requests.post(AMZN_API['LWA_API_TOKEN'], json={
                'grant_type': 'refresh_token',
                'refresh_token': config['AMZN']['refresh_token'],
                'client_id': config['AMZN']['client_id'],
                'client_secret': config['AMZN']['client_secret'],
            })

            if res.status_code == 200:
                json_res = res.json()
                access_token = json_res['access_token']

                return access_token

            elif res.status_code == 401:
                raise AmzApiAuthenticationException

        except Exception as e:
            raise e

    def __get_rdt_api_token(self, lwa_api_token, method, path):
        try:
            headers = {
                'x-amz-access-token': lwa_api_token
            }

            data = {
                "restrictedResources": [
                    {
                        "method": method,
                        "path": path
                    }
                ]
            }

            res = requests.post(AMZN_API['RDT_API_TOKEN'], headers=headers, json=data)

            if res.status_code == 200:
                json_res = res.json()
                access_token = json_res['restrictedDataToken']

                return access_token

            elif res.status_code == 401:
                raise AmzApiAuthenticationException

        except Exception as e:
            raise e
