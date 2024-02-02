from tikapi import TikAPI, ValidationException, ResponseException
from common.util.get_config import get_config
from common.util.logger_get import get_logger

config = get_config()
logger = get_logger()

def get_profile_stat():
    api_key = config['TIKAPI']['api_key']
    account_key = config['TIKAPI']['account_key']
    api = TikAPI(api_key)
    User = api.user(accountKey=account_key)

    try:
        response = User.info()

        # if response.status == 'success':
        if response.status_code == 200:
            return response.json()

    except ValidationException as e:
        print(e, e.field)
        raise e

    except ResponseException as e:
        print(e, e.response.status_code)
        raise e
