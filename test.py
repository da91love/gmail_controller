from tikapi import TikAPI, ValidationException, ResponseException
from common.util.get_config import get_config

config = get_config()

api_key = config['TIKAPI']['api_key']
account_key = config['TIKAPI']['account_key']
api = TikAPI(api_key)
User = api.user(accountKey=account_key)

try:
    response = User.posts.video(
        id="7327368161349913902"
    )

    res = response.json()
    print(res)

except ValidationException as e:
    print(e, e.field)

except ResponseException as e:
    print(e, e.response.status_code)