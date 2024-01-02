import requests
from datetime import datetime
from operator import itemgetter
import json
import pydash as _

from common.lib.ma.data_access.system.AccessService import AccessService
from api_gmail_checker.const.slack_contents import *
from common.slack import Slack

def slack_wrapper(mail_res):
    try:
        gmail_thread_id = mail_res.get('gmail_thread_id')
        gmail_msg_id = mail_res.get('gmail_msg_id')
        author_unique_id = mail_res.get('author_unique_id')
        gmail_label_id = mail_res.get('gmail_label_id')
        seeding_num = mail_res.get('seeding_num')
        tg_brand = mail_res.get('tg_brand')
        contents = mail_res.get('contents')

        # declare instance
        slack = Slack()

        # Slack history 데이터 취득
        slack_thread_history = AccessService.select_slack_thread_history(gmail_thread_id=gmail_thread_id)

        # Slack에 채워넣을 데이터 취득
        ## 메일, 틱톡 url 등
        slack_need_info = AccessService.select_slack_need_info(author_unique_id=author_unique_id, seeding_num=seeding_num, tg_brand=tg_brand)[0]
        receiver_email, tiktok_url, pic = itemgetter('receiver_email', 'tiktok_url', 'pic')(slack_need_info)

        ## status 데이터 취득
        contact_status = AccessService.select_contact_status(gmail_thread_id=gmail_thread_id)[0]
        status, progress = itemgetter('status', 'progress')(contact_status)

        # Slack thread
        if len(slack_thread_history) > 0:
            if len(_.filter_(slack_thread_history, {'gmail_msg_id': gmail_msg_id})) > 0:
                pass
            else:
                slack_thread_id = slack_thread_history[0]['slack_thread_id']
                msg = json.dumps(get_mail_reply_slack_block(gmail_label_id, contents))

                # sent이면 메세지 내용 수정
                if gmail_label_id == 'SENT':
                    update_msg = json.dumps(get_mail_sent_slack_block(tiktok_url, author_unique_id, receiver_email, status, progress, pic))
                    slack_res = slack.update_post('C068UMGLCDQ', 'block', update_msg, slack_thread_id)

                slack_res = slack.add_reply('C068UMGLCDQ', 'block', msg, slack_thread_id)

                if slack_res.status_code == 200:
                    formatted_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    AccessService.insert_slack_thread_id(
                        slack_thread_id=slack_thread_id,
                        gmail_thread_id=gmail_thread_id,
                        gmail_msg_id=gmail_msg_id,
                        created_at=formatted_datetime
                    )

        else:
            msg = json.dumps(get_mail_arrive_slack_block(tiktok_url, author_unique_id, receiver_email, status, progress, pic))
            slack_res = slack.add_post('C068UMGLCDQ', 'block', msg)

            if slack_res.status_code == 200:
                slack_thread_id = slack_res.text

                # create slack reply
                reply_msg = json.dumps(get_mail_reply_slack_block(gmail_label_id, contents))
                slack_res = slack.add_reply('C068UMGLCDQ', 'block', reply_msg, slack_thread_id)

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