# import boto3
from multiprocessing import Pool, Queue, Manager
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(api_root)


from api_post_stat_tracker.get_post_stat import get_post_stat
from common.util.get_config import get_config
from common.util.logger_get import get_logger
from common.lib.ma.data_access.system.AccessService import AccessService

# Create instance
config = get_config()
logger = get_logger()

if __name__ == "__main__":
    posts_info = [i['post_id'] for i in AccessService.select_post_info()]

    with Manager() as manager:
        # Create a multiprocessing pool with a specified number of processes
        num_processes = 10  # Adjust this based on your system's capabilities
        pool = Pool(processes=num_processes)

        # multi process sentiments
        try:
            # Use the pool to send requests to the API URLs
            args = [(i,) for i in posts_info]
            entity_results = pool.map(get_post_stat, args)
        except Exception as e:
            print("Exception in worker processes:", e)
        finally:
            # Close the pool and wait for the worker processes to finish
            pool.close()
            pool.join()

    # Get result from manager
    sentiment_results = list(entity_results)

    print(sentiment_results)