
# import boto3
import csv
import uuid
from datetime import datetime
from operator import itemgetter
import pydash as _
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(api_root)

from common.AppBase import AppBase
from common.type.Errors import *
from common.util.get_config import get_config
from common.gmail.send_email import send_email
from common.gmail.LabelControl import LabelControl
from api_gmail_sender.type.ResType import ResType
from api_gmail_sender.const.mail_info import *
from common.const.EMAIL import *
from common.const.STATUS import *

from common.lib.ma.data_access.system.AccessService import AccessService

# Create instance
config = get_config()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

# 과거에 답장온 회수가 1회 이상이고, status가 open인 대상에게 메일 변경 안내 메일 송신
all_contact = AccessService.select_temp()
contact_history_by_group = _.group_by(all_contact, 'gmail_thread_id')

loop = 0
for thread_id in contact_history_by_group:
    # status
    ## 기존꺼 삭제
    AccessService.delete_temp_status(old_gmail_thread_id=thread_id)
    ## 새로운거 없으면 추가
    AccessService.insert_contact_status(gmail_thread_id=thread_id, status='open', progress='negotiating')

    loop += 1
    print(loop)
