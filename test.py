
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
    response = User.posts.video(
        id="7338573931630038277"
    )

    data = response.json()

    if data:
        payload = data['itemInfo']['itemStruct']
        if payload:
            post_id = payload['id']
            posted_time = DateUtil.ten_digit_2_Ymdhms(payload['createTime'])
            collect_count = payload['stats']['collectCount']
            comment_count = payload['stats']['commentCount']
            digg_count = payload['stats']['diggCount']
            play_count = payload['stats']['playCount']
            share_count = payload['stats']['shareCount']
            tags = ','.join([d['hashtagName'] for d in payload.get('textExtra')]) if payload.get('textExtra') else ''

            result = {
                'post_id': post_id,
                'posted_time':posted_time,
                'collect_count':collect_count,
                'comment_count':comment_count,
                'digg_count':digg_count,
                'play_count':play_count,
                'share_count':share_count,
                'tags':tags
            }

            print(result)


except ValidationException as e:
    print(e, e.field)

except ResponseException as e:
    print(e, e.response.status_code)

