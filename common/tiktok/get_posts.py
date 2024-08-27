from tikapi import TikAPI, ValidationException, ResponseException
from common.util.get_config import get_config
from common.util.logger_get import get_logger
from common.util.DateUtil import *
from datetime import date, timedelta

config = get_config()
logger = get_logger()

def get_posts(uniq_id: str, day_bf_until: int):
    api_key = config['TIKAPI']['api_key']
    api = TikAPI(api_key)

    posts = []
    today = date.today()
    date_bf = today - timedelta(days=day_bf_until)
    date_bf_1_day = today - timedelta(days=2)

    try:
        user_info_res = api.public.check(username=uniq_id)

        # if response.status == 'success':
        if user_info_res.status_code == 200:
            user_info_res_as_json = user_info_res.json()
            secUid = user_info_res_as_json.get('userInfo').get('user').get('secUid')

            posts_res = api.public.posts(secUid=secUid)

            if posts_res.status_code == 200:

                stop_processing = False
                while (posts_res):
                    posts_res_as_json = posts_res.json()

                    for post_info in posts_res_as_json.get('itemList'):
                        if not post_info.get('isPinnedItem'):
                            createTime = DateUtil.ten_digit_2_Ymd(post_info.get('createTime'))
                            parsed_createTime = datetime.strptime(createTime, "%Y-%m-%d").date()

                            # createTime 형식 변경
                            post_info['createTime'] = parsed_createTime

                            # 코드에서 뽑는 시간은 한국 시간이고 틱톡에서 받는 시간은 PST시간으로 타임라인 상이함에 유의
                            # 게시후 24시간 이전인 게시글은 수집에서 제외
                            if parsed_createTime < date_bf_1_day:
                                if date_bf <= parsed_createTime:
                                    posts.append(post_info)
                                else:
                                    stop_processing = True
                                    break

                    if stop_processing:
                        break  # Breaks out of the while loop

                    cursor = posts_res.json().get('cursor')
                    print("Getting next items ", cursor)
                    posts_res = posts_res.next_items()

            else:
                raise Exception
        else:
            raise Exception

        return posts

    except ValidationException as e:
        print(e)

    except ResponseException as e:
        print(e)

    except Exception as e:
        print(e)