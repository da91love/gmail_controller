from datetime import datetime
from operator import itemgetter
import pydash as _

from common.util.logger_get import get_logger
from common.type.Errors import *
from common.lib.ma.data_access.system.AccessService import AccessService
from common.slack.SlackMsgCreator import SlackMsgCreator
from common.slack.Slack import Slack
from common.const.SLACK import *
from common.util.StrUtil import StrUtil

logger = get_logger()

def slack_wrapper(slack_info, slack_chn_id):
    try:
        gmail_thread_id = slack_info.get('gmail_thread_id')
        gmail_msg_id = slack_info.get('gmail_msg_id')
        gmail_label_id = slack_info.get('gmail_label_id')
        created_at = slack_info.get('created_at')
        t_key = slack_info.get('t_key')
        contents = slack_info.get('contents')

        # declare instance
        slack = Slack()

        # Slack history 데이터 취득
        slack_thread_history = AccessService.select_slack_thread_history(gmail_thread_id=gmail_thread_id)

        # Slack에 채워넣을 데이터 취득
        ## 메일, 틱톡 url 등
        slack_need_info = AccessService.select_slack_need_info(t_key=t_key)[0]
        author_unique_id, receiver_email, sender_email, tiktok_url, pic \
            = itemgetter('author_unique_id', 'receiver_email', 'sender_email', 'tiktok_url', 'pic')(slack_need_info)

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
                update_msg = SlackMsgCreator.get_slack_contact_post_block(
                    tiktok_url=tiktok_url,
                    author_unique_id=author_unique_id,
                    receiver_email=receiver_email,
                    sender_email=sender_email,
                    status=status,
                    progress=progress,
                    pic=pic,
                    is_reply_done=is_reply_done,
                )
                slack_update_res = slack.update_post(slack_chn_id, MSG_TYPE['BLOCK'], update_msg, slack_thread_id)
                if slack_update_res.status_code == 200:

                    for contents_chunk in StrUtil.split_string_into_chunks(contents):
                        reply_msg = SlackMsgCreator.get_slack_contact_reply_block(
                            gmail_label_id=gmail_label_id,
                            sender_email=sender_email,
                            created_at=created_at,
                            contents=contents_chunk,
                        )

                        slack_reply_res = slack.add_reply(slack_chn_id, MSG_TYPE['BLOCK'], reply_msg, slack_thread_id)

                        if slack_reply_res.status_code != 200:
                            raise SlackApiInternalException(msg=slack_reply_res.text)

                    # if slack reply does not have error
                    AccessService.insert_slack_thread_id(
                        slack_thread_id=slack_thread_id,
                        gmail_thread_id=gmail_thread_id,
                        gmail_msg_id=gmail_msg_id,
                        created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    )

                else:
                    raise SlackApiInternalException(msg=slack_update_res.text)

        else:
            post_msg = SlackMsgCreator.get_slack_contact_post_block(
                tiktok_url=tiktok_url,
                author_unique_id=author_unique_id,
                receiver_email=receiver_email,
                sender_email=sender_email,
                status=status,
                progress=progress,
                pic=pic,
                is_reply_done=is_reply_done,
            )
            slack_res = slack.add_post(slack_chn_id, MSG_TYPE['BLOCK'], post_msg)

            if slack_res.status_code == 200:
                slack_thread_id = slack_res.text

                for contents_chunk in StrUtil.split_string_into_chunks(contents):
                    reply_msg = SlackMsgCreator.get_slack_contact_reply_block(
                        gmail_label_id=gmail_label_id,
                        sender_email=sender_email,
                        created_at=created_at,
                        contents=contents_chunk,
                    )

                    slack_reply_res = slack.add_reply(slack_chn_id, MSG_TYPE['BLOCK'], reply_msg, slack_thread_id)
                    if slack_reply_res.status_code != 200:
                        raise SlackApiInternalException(msg=slack_reply_res.text)

                # if slack reply does not have error
                AccessService.insert_slack_thread_id(
                    slack_thread_id=slack_thread_id,
                    gmail_thread_id=gmail_thread_id,
                    gmail_msg_id=gmail_msg_id,
                    created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )

            else:
                raise SlackApiInternalException(msg=slack_res.text)

            return True
    except Exception as e:
        raise