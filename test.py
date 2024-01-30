from tikapi import TikAPI, ValidationException, ResponseException
from common.util.get_config import get_config
from common.util.logger_get import get_logger

config = get_config()
logger = get_logger()


api_key = config['TIKAPI']['api_key']
account_key = config['TIKAPI']['account_key']
api = TikAPI(api_key)
User = api.user(accountKey=account_key)

try:
    response = api.public.search(
        category="general",
        query="cosrx",
        country='us'
    )

    while(response):
        res = response.json()
        nextCursor = response.json().get('nextCursor')
        print("Getting next items ", nextCursor)
        response = response.next_items()

except ValidationException as e:
    print(e, e.field)

except ResponseException as e:
    print(e, e.response.status_code)