import requests
from datetime import datetime
from operator import itemgetter
import json

from common.lib.ma.data_access.system.AccessService import AccessService
from api_gmail_checker.const.slack_contents import get_formatted_block
from common.const.API_URL import SLACK_URL

def slack_wrapper(mail_res):
    try:
        gmail_thread_id = mail_res.get('gmail_thread_id')

        infl_info = AccessService.select_infl_info(gmail_thread_id= gmail_thread_id)[-1]
        author_unique_id, receiver_email, tiktok_url \
            = itemgetter('author_unique_id', 'receiver_email', 'tiktok_url')(infl_info)

        # format mail body
        formatted_block = json.dumps(get_formatted_block(tiktok_url, author_unique_id, receiver_email))

        slack_res = requests.post(SLACK_URL, data={
            'type': 'block',
            'channel': 'C068UMGLCDQ',
            'msg': formatted_block
        })

        if slack_res.status_code == 200:
            slack_thread_id = slack_res.text

            formatted_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            AccessService.insert_slack_thread_id(
                slack_thread_id= slack_thread_id,
                gmail_thread_id= gmail_thread_id,
                create_at= formatted_datetime
            )

        return True
    except Exception as e:
        raise