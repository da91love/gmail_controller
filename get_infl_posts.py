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
from common.const.DB import *
from common.util.DateUtil import DateUtil

# Create instance
config = get_config()
logger = get_logger()

if __name__ == "__main__":
    print('klk')