# import boto3
import csv
import uuid
from multiprocessing import Pool, Queue, Manager
from tikapi import TikAPI, ValidationException, ResponseException
import os
import sys
from mysql.connector.errors import *
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(api_root)


from api_post_stat_tracker.type.ResType import ResType
from api_post_stat_tracker.get_post_stat import get_post_stat
from common.AppBase import AppBase
from common.type.Errors import *
from common.util.get_config import get_config
from common.util.logger_get import get_logger
from common.lib.ma.data_access.system.AccessService import AccessService

# Create instance
config = get_config()
logger = get_logger()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

@AppBase
def app_api_post_stat_tracker(event, context=None):
    """
    lambda_handler : This functions will be implemented in lambda
    :param event: (dict)
    :param context: (dict)
    :return: (dict)
    """

    if __name__ == "__main__":
        # Get data from API Gateway
        eventdata = event

        posts_info = AccessService.select_post_info()

        with Manager() as manager:
            managing_list = manager.list()

            # Create a multiprocessing pool with a specified number of processes
            num_processes = 10  # Adjust this based on your system's capabilities
            queue = Queue()
            pool = Pool(processes=num_processes)

            # multi process sentiments
            ## Use the pool to send requests to the API URLs
            args = [(post_info['id'],) for post_info in posts_info]
            pool.map(get_post_stat, args)

            ## Close the pool and wait for the worker processes to finish
            pool.close()
            pool.join()

        # Get result from manager
        sentiment_results = list(managing_list)

        print(sentiment_results)

        return ResType(data=[]).get_response()

# result = app_api_delivery_tracker(None)
# print(result)