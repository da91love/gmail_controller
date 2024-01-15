
import requests
from common.const.API_URL import *
from common.util.get_config import get_config

config = get_config()
class Amazon:
    def __init__(self, ):
        pass

    def get_tracking_details(self, tracking_id):
        try:
            api_token = self.__get_rdt_api_token(
                lwa_api_token=self.__get_lwa_api_token(),
                method='GET',
                path='/shipping/v1/tracking/{trackingId}'
            )

            headers = {
                'x-amz-access-token': api_token
            }

            api_url = f'https://sellingpartnerapi-na.amazon.com/shipping/v1/tracking/{tracking_id}'

            res = requests.get(api_url, headers=headers)

            if res.status_code == 200:
                res_json = res.json()
                return res_json

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

        except Exception as e:
            raise e
