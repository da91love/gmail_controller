import json
import html

from common.const.STATUS import *

class SlackMsgCreator:
    @staticmethod
    def get_slack_contact_post_block(tiktok_url, author_unique_id, receiver_email, sender_email, status, progress, pic, is_reply_done):
        return json.dumps([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{'~Conversation with <'+tiktok_url+'|'+author_unique_id+'> is started!~' if status == STATUS['CLOSE'] else '*Conversation with <'+tiktok_url+'|'+author_unique_id+'> is started!*'}"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ Influence name* : <{tiktok_url}|{author_unique_id}>"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ Receiver mail address* : {receiver_email}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ Sender mail address* : {sender_email}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ Reply* : {'*REPLY DONE* 🟢' if is_reply_done else '*REPLY NECESSARY* 🔴'}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ status* : {status}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ progress* : {progress}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ Person In Charge* : {pic}"
                }
            }
        ])

    @staticmethod
    def get_slack_contact_reply_block(gmail_label_id, sender_email, created_at, contents):
        contents = html.unescape(contents)

        return json.dumps([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ MAIL status:* {gmail_label_id}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ Sender mail address:* {sender_email}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ MAIL time:* {created_at}"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ contents* : {contents}"
                }
            }
        ])

    @staticmethod
    def get_slack_remind_post_block(tiktok_url, gmail_label_id, author_unique_id, receiver_email, sender_email, pic, status, progress, created_at):
        return json.dumps([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*CONTACT REMIND: contact with below user has been over 3days. Please check out the status.*"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ Influence name* : <{tiktok_url}|{author_unique_id}>"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ Label* : {gmail_label_id}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ Receiver mail address* : {receiver_email}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ Sender mail address* : {sender_email}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ Person In Charge* : {pic}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ status* : {status}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ progress* : {progress}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ Last contact date* : {created_at}"
                }
            }
        ])

    @staticmethod
    def get_slack_tiktok_kpi_post_block(
            today: str,
            today_contact_count: int,
            future_contact_count: int,
            cnct_count: int,
            delivery_count: int,
            post_count: int,
            post_url: str,
            this_week_posts,
            this_week_play_count,
            last_week_posts,
            last_week_play_count,
    ):
        return json.dumps([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*이퀄베리 EA {today} 실적 보고♡*"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"・ 금일 신규 메일 송신 회수: *{today_contact_count}회 (남은 메일: {future_contact_count})*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"・ 컨택 회수: *{cnct_count}회*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"・ 신규계약건수: *{delivery_count}건*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"・ 금일 업로드 포스트: *{post_count}건* ({post_url})"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"・ 금주 업로드 포스트수 누적: *{this_week_posts}건*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"・ 금주 업로드 뷰수 누적: *{this_week_play_count}회*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"・ 지난주 업로드 포스트수 누적: *{last_week_posts}건*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"・ 금주 업로드 뷰수 누적: *{last_week_play_count}회*"
                }
            }
        ])
