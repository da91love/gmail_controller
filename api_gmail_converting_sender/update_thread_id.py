
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
from common.const.DB import *

# Create instance
config = get_config()

# get config data
# s3_bucket_name = config['S3']['s3_bucket_name']

# 모든 mail contact 검색
all_contact = AccessService(GLOBAL).select_temp()
contact_history_by_group = _.group_by(all_contact, 't_key')

loop = 0
for t_key in contact_history_by_group:
    tg_contact_histories = contact_history_by_group[t_key]
    thread_ids = [i['gmail_thread_id'] for i in tg_contact_histories]
    uniq_thread_ids = _.uniq(thread_ids)

    if len(uniq_thread_ids) > 1:
        sorted_contact_histories = _.sort_by(tg_contact_histories, 'created_at')
        new_gmail_thread_id = sorted_contact_histories[-1].get('gmail_thread_id')

        for tg_thread_id in uniq_thread_ids:
            old_gmail_thread_id = tg_thread_id
            print('new_gmail_thread_id: '+new_gmail_thread_id)
            print('old_gmail_thread_id: '+old_gmail_thread_id)

            # mail contents
            AccessService(GLOBAL).update_gmail_mail_contents_thread_id(new_gmail_thread_id=new_gmail_thread_id, old_gmail_thread_id=old_gmail_thread_id)

            # mail contact
            AccessService(GLOBAL).update_gmail_mail_contact_thread_id(new_gmail_thread_id=new_gmail_thread_id, old_gmail_thread_id=old_gmail_thread_id)

            loop += 1
            print(loop)