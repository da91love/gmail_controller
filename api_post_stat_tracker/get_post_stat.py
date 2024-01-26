from tikapi import TikAPI, ValidationException, ResponseException
from common.util.get_config import get_config
from common.util.logger_get import get_logger

config = get_config()
logger = get_logger()

def get_post_stat(id_set: set):
    api_key = config['TIKAPI']['api_key']
    account_key = config['TIKAPI']['account_key']
    api = TikAPI(api_key)
    User = api.user(accountKey=account_key)

    id = id_set[0]

    try:
        response = User.posts.video(id=id)

        # if response.status == 'success':
        if response.status_code == 200:
            return {
                'data': response.json(),
                'post_id': id
            }
        else:
            return {
                'data': None,
                'post_id': id
            }

        # else:
        #     logger.info('fail')

    except ValidationException as e:
        return {
            'data': None,
            'post_id': id
        }


    except ResponseException as e:
        return {
            'data': None,
            'post_id': id
        }
