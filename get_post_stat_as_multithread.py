# import boto3
from multiprocessing import Pool, Queue, Manager
import pydash as _
from datetime import datetime
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(api_root)

from common.tiktok.get_post_stat import get_post_stat
from common.util.get_config import get_config
from common.util.logger_get import get_logger
from common.lib.ma.data_access.system.AccessService import AccessService
from common.util.DateUtil import DateUtil

# Create instance
config = get_config()
logger = get_logger()

if __name__ == "__main__":
    tg_posts_info = []
    posts_info = AccessService.select_post_info()
    posts_history_grouped_by_id = _.group_by(AccessService.select_posting_history(), 'post_id')
    for post_info in posts_info:
        # 1차 필터링: post_type 비디오만 취득
        post_type = post_info['post_type']
        if post_type == 'video':
            post_history = posts_history_grouped_by_id.get(post_info['post_id'])
            # 2차 필터링 : post history 1개 라도 존재하면 3차필터링으로, 아니면 대상 추가
            if post_history:
                posted_time = post_history[0]['posted_time']
                day_diff = (datetime.now() - posted_time).days
                # 3차 필터링: 게시날이 7일 이내일 것
                if day_diff <= 7:
                    tg_posts_info.append(post_info)
            else:
                tg_posts_info.append(post_info)

    tg_posts_id = [i['post_id'] for i in tg_posts_info]

    with Manager() as manager:
        # Create a multiprocessing pool with a specified number of processes
        num_processes = 10  # Adjust this based on your system's capabilities
        pool = Pool(processes=num_processes)

        # multi process sentiments
        try:
            # Use the pool to send requests to the API URLs
            args = [(i,) for i in tg_posts_id]
            results = pool.map(get_post_stat, args)
        except Exception as e:
            print("Exception in worker processes:", e)
        finally:
            # Close the pool and wait for the worker processes to finish
            pool.close()
            pool.join()

    # Get result from manager
    posts_stat = list(results)

    for post_stat in posts_stat:
        # TODO: data 비었을 시 errorhandling 필요
        data = post_stat['data']
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

                AccessService.insert_posting_history(
                    post_id=post_id,
                    posted_time=posted_time,
                    collect_count=collect_count,
                    comment_count=comment_count,
                    digg_count=digg_count,
                    play_count=play_count,
                    share_count=share_count,
                    tags=tags
                )