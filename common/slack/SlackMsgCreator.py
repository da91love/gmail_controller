import json

from common.const.STATUS import *

class SlackMsgCreator:
    @staticmethod
    def get_slack_post_block(tiktok_url, author_unique_id, receiver_email, sender_email, status, progress, pic, is_reply_done):
        return json.dumps([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{'~Coversation with <'+tiktok_url+'|'+author_unique_id+'> is started!~' if status == STATUS['CLOSE'] else '*Coversation with <'+tiktok_url+'|'+author_unique_id+'> is started!*'}"
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
    def get_slack_reply_block(gmail_label_id, sender_email, created_at, contents):
        return json.dumps([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"* MAIL status: {gmail_label_id}*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"* Sender mail address: {sender_email}*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"* MAIL time: {created_at}*"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ contents* : <{contents}>"
                }
            }
        ])
