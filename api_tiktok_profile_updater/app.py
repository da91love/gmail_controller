# import boto3
import csv
import uuid
from operator import itemgetter
import os
import sys
from mysql.connector.errors import *
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(api_root)


from api_tiktok_profile_updater.type.ResType import ResType
from common.AppBase import AppBase
from common.tiktok.get_profile_stat import get_profile_stat
from common.util.get_config import get_config
from common.util.logger_get import get_logger
from common.lib.ma.data_access.system.AccessService import AccessService

# Create instance
config = get_config()
logger = get_logger()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def app_api_tiktok_profile_updater(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    # Get data from API Gateway
    eventdata = event

    profile_info = get_profile_stat().get('userInfo')

    user = profile_info.get('user')
    stats = profile_info.get('stats')

    id, author_unique_id = itemgetter('id', 'uniqueId')(user)

    digg_count, follower_count, following_count, friend_count, heart, heart_count, video_count \
            = itemgetter('diggCount', 'followerCount', 'followingCount', 'friendCount', 'heart', 'heartCount', 'videoCount')(stats)


    AccessService.insert_profile_stats(
        id=id,
        author_unique_id=author_unique_id,
        digg_count=digg_count,
        follower_count=follower_count,
        following_count=following_count,
        friend_count=friend_count,
        heart=heart,
        heart_count=heart_count,
        video_count=video_count
    )

    return ResType().get_response()

# result = app_api_delivery_tracker(None)
# print(result)