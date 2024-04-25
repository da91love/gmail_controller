# import boto3
from multiprocessing import Pool, Queue, Manager
from mysql.connector.errors import IntegrityError
import random
import pydash as _
from datetime import datetime
import os
import sys
import uuid
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(api_root)

from common.tiktok.get_public_search import get_public_search
from common.tiktok.get_public_hashtag import get_public_hashtag
from common.util.get_config import get_config
from common.util.logger_get import get_logger
from common.lib.ma.data_access.system.AccessService import AccessService
from common.util.DateUtil import DateUtil
from common.util.LogicUtil import LogicUtil
from config.development import *

# Create instance
config = get_config()
logger = get_logger()

if __name__ == "__main__":
    tags = ['skin1004','manyo', 'torriden', 'tocobo', 'aestura', 'banilaco', 'mixsoon', 'numbuzin', 'tirtir', 'anua', 'somebymi', 'mediheal']

    pic_email_match = AccessService.select_pic_email_match()

    with Manager() as manager:
        # Create a multiprocessing pool with a specified number of processes
        num_processes = 10  # Adjust this based on your system's capabilities
        pool = Pool(processes=num_processes)

        # multi process sentiments
        try:
            # Use the pool to send requests to the API URLs
            args = [(tag,) for tag in tags]
            results = pool.map(get_public_search, args)
        except Exception as e:
            print("Exception in worker processes:", e)
        finally:
            # Close the pool and wait for the worker processes to finish
            pool.close()
            pool.join()

    # Get result from manager
    posts_stat = _.flatten_deep(list(results))

    new_infl = []
    hash_tags = []
    for post_stat in posts_stat:

        try:
            # TODO: data 비었을 시 errorhandling 필요
            posted_time = DateUtil.ten_digit_2_Ymdhms(post_stat['createTime'])
            posted_time_as_date = datetime.strptime(posted_time, "%Y-%m-%d %H:%M:%S")

            text_extra = post_stat.get('textExtra')
            if text_extra: [hash_tags.append(t['hashtagName']) for t in text_extra]

            day_diff = (datetime.now() - posted_time_as_date).days
            if day_diff <= 30:
                receiver_email = LogicUtil.extract_email(post_stat['author']['signature'])
                if receiver_email:
                    t_key = "auto" + (str(uuid.uuid4()))[4:]
                    author_unique_id = post_stat['author']['uniqueId']
                    tiktok_url = f'https://www.tiktok.com/@{author_unique_id}/video/{post_stat["id"]}'

                    # set sender email and pic
                    ran_num = random.randint(0, 3)
                    sender_email = pic_email_match[ran_num]['sender_email']
                    pic = pic_email_match[ran_num]['pic']

                    try:
                        AccessService.insert_infl_contact_info(
                            t_key=t_key,
                            author_unique_id=author_unique_id,
                            seeding_num=1,
                            tg_brand='eqqualberry',
                            channel='tiktok',
                            tg_country='US',
                            receiver_email=receiver_email,
                            tiktok_url=tiktok_url,
                            source_type='post',
                            sender_email=sender_email,
                        )

                        AccessService.insert_pic(
                            t_key=t_key,
                            pic=pic
                        )

                        logger.info({
                            'author_unique_id': author_unique_id,
                            'receiver_email': receiver_email,
                            'tiktok_url': tiktok_url
                        })
                    except IntegrityError as e:
                        logger.error(e)
                        continue

        except TypeError as e:
            logger.error(e)
            continue

        except Exception as e:
            logger.error(e)
            raise e

    logger.info(_.uniq(hash_tags))
