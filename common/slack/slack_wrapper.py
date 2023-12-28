import requests
from datetime import datetime
from operator import itemgetter
import json
import pydash as _

from common.lib.ma.data_access.system.AccessService import AccessService
from api_gmail_checker.const.slack_contents import *
from common.const.API_URL import SLACK_URL

def slack_wrapper(mail_res):
    try:
        gmail_thread_id = mail_res.get('gmail_thread_id')
        gmail_msg_id = mail_res.get('gmail_msg_id')
        author_unique_id = mail_res.get('author_unique_id')
        gmail_label_id = mail_res.get('gmail_label_id')
        seeding_num = mail_res.get('seeding_num')
        contents = mail_res.get('contents')

        slack_thread_history = AccessService.select_slack_thread_history(gmail_thread_id=gmail_thread_id)

        # Slack thread
        if len(slack_thread_history) > 0:
            if len(_.filter_(slack_thread_history, {'gmail_msg_id': gmail_msg_id})) > 0:
                pass
            else:
                slack_thread_id = slack_thread_history[0]['slack_thread_id']

                slack_res = requests.post(SLACK_URL, data={
                    'type': 'block',
                    'channel': 'C068UMGLCDQ',
                    'msg': json.dumps(get_mail_reply_slack_block(gmail_label_id, contents)),
                    'thread_ts': slack_thread_id
                })

                if slack_res.status_code == 200:
                    formatted_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    AccessService.insert_slack_thread_id(
                        slack_thread_id=slack_thread_id,
                        gmail_thread_id=gmail_thread_id,
                        gmail_msg_id=gmail_msg_id,
                        created_at=formatted_datetime
                    )

        else:
            slack_need_info = AccessService.select_slack_need_info(author_unique_id= author_unique_id, seeding_num=seeding_num)[0]
            receiver_email, tiktok_url, gmail_msg_id = itemgetter('receiver_email', 'tiktok_url', 'gmail_msg_id')(slack_need_info)

            slack_res = requests.post(SLACK_URL, data={
                'type': 'block',
                'channel': 'C068UMGLCDQ',
                'msg': json.dumps(get_mail_arrive_slack_block(tiktok_url, author_unique_id, receiver_email))
            })

            if slack_res.status_code == 200:
                slack_thread_id = slack_res.text

                # create slack reply
                requests.post(SLACK_URL, data={
                    'type': 'block',
                    'channel': 'C068UMGLCDQ',
                    'msg': json.dumps(get_mail_reply_slack_block(gmail_label_id, contents)),
                    'thread_ts': slack_thread_id
                })

                formatted_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                AccessService.insert_slack_thread_id(
                    slack_thread_id= slack_thread_id,
                    gmail_thread_id= gmail_thread_id,
                    gmail_msg_id=gmail_msg_id,
                    created_at= formatted_datetime
                )

            return True
    except Exception as e:
        raise