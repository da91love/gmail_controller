
from tikapi import TikAPI, ValidationException, ResponseException
from common.util.get_config import get_config
from common.util.EncodingUtil import EncodingUtil
from common.util.logger_get import get_logger
from common.util.DateUtil import DateUtil

config = get_config()
logger = get_logger()


api_key = config['TIKAPI']['api_key']
account_key = config['TIKAPI']['account_key']
api = TikAPI(api_key)
User = api.user(accountKey=account_key)

try:
    res = User.posts.comments.list(
        media_id="7338573931630038277"
    )

    while(res):
        cursor = res.json().get('cursor')
        print("Getting next items ", cursor)
        res = res.next_items()

except ValidationException as e:
    print(e, e.field)

except ResponseException as e:
    print(e, e.response.status_code)

