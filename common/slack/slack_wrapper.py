from datetime import datetime
from operator import itemgetter
import pydash as _

from common.lib.ma.data_access.system.AccessService import AccessService
from common.slack.SlackMsgCreator import SlackMsgCreator
from common.slack.Slack import Slack
from common.const.SLACK import *

def slack_wrapper(mail_res):
    try:
        gmail_thread_id = mail_res.get('gmail_thread_id')
        gmail_msg_id = mail_res.get('gmail_msg_id')
        gmail_label_id = mail_res.get('gmail_label_id')
        t_key = mail_res.get('t_key')
        contents = mail_res.get('contents')

        # declare instance
        slack = Slack()

        # Slack history 데이터 취득
        slack_thread_history = AccessService.select_slack_thread_history(gmail_thread_id=gmail_thread_id)

        # Slack에 채워넣을 데이터 취득
        ## 메일, 틱톡 url 등
        slack_need_info = AccessService.select_slack_need_info(t_key=t_key)[0]
        author_unique_id, receiver_email, tiktok_url, pic = itemgetter('author_unique_id', 'receiver_email', 'tiktok_url', 'pic')(slack_need_info)

        ## status 데이터 취득
        contact_status = AccessService.select_contacts_status(gmail_thread_id=gmail_thread_id)[0]
        status, progress = itemgetter('status', 'progress')(contact_status)

        ## is reply done
        is_reply_done = True if gmail_label_id == 'SENT' else False

        # Slack thread
        if len(slack_thread_history) > 0:
            # 이미 reply 처리된 gmail_msg_id 존재시 pass
            if len(_.filter_(slack_thread_history, {'gmail_msg_id': gmail_msg_id})) == 0:
                slack_thread_id = slack_thread_history[0]['slack_thread_id']
                msg = SlackMsgCreator.get_slack_reply_block(gmail_label_id, contents)

                update_msg = SlackMsgCreator.get_slack_post_block(tiktok_url, author_unique_id, receiver_email, status, progress, pic, is_reply_done)
                slack.update_post(CHANNEL_ID, MSG_TYPE['BLOCK'], update_msg, slack_thread_id)

                slack_res = slack.add_reply(CHANNEL_ID, MSG_TYPE['BLOCK'], msg, slack_thread_id)

                if slack_res.status_code == 200:
                    formatted_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    AccessService.insert_slack_thread_id(
                        slack_thread_id=slack_thread_id,
                        gmail_thread_id=gmail_thread_id,
                        gmail_msg_id=gmail_msg_id,
                        created_at=formatted_datetime
                    )

        else:
            msg = SlackMsgCreator.get_slack_post_block(tiktok_url, author_unique_id, receiver_email, status, progress, pic, is_reply_done)
            slack_res = slack.add_post(CHANNEL_ID, MSG_TYPE['BLOCK'], msg)

            if slack_res.status_code == 200:
                slack_thread_id = slack_res.text

                # create slack reply
                reply_msg = SlackMsgCreator.get_slack_reply_block(gmail_label_id, contents)
                slack.add_reply(CHANNEL_ID, MSG_TYPE['BLOCK'], reply_msg, slack_thread_id)

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