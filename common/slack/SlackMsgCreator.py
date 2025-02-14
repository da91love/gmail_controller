import json
import html

from common.const.STATUS import *

class SlackMsgCreator:
    @staticmethod
    def get_slack_updated_shipment_request():

        return json.dumps([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "출고 요청이 업데이트 되었습니다.\n<@U070KTKCD5L><@U07B2HY3E3F>"
                }
            }
        ])

    @staticmethod
    def get_slack_delivery_request_post_block(pic, export_no, buyer_name, address, recipient, phone_num, requested_arrival_date, bill_type, related_docs, remark):

        return json.dumps([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "신규 출고 요청이 생성되었습니다.\n<@U070KTKCD5L><@U07B2HY3E3F>"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"`요청자` : {pic}\n`수출번호` : {export_no}\n`업체명` : {buyer_name}\n`입고지` : {address}\n`입고지담당자` : {recipient}\n`담당자연락처` : {phone_num}\n`출고요청일` : {requested_arrival_date}\n`필요서류` : {bill_type}\n`출고요청서 링크` : https://drive.google.com/drive/folders/{related_docs}\n`특이사항` : {remark}"
                }
            },
            {
                "type": "divider"
            }
        ])

    @staticmethod
    def get_slack_new_invoice_details_reply_block(productName, productCode, quantity):

        return json.dumps([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"\n`품목명` : {productName}\n`품목코드` : {productCode}\n`수량` : {quantity}\n"
                }
            }
        ])

    @staticmethod
    def get_slack_new_invoice_post_block(pi_request_date, pi_no, export_no, buyer_name, country, summed_amount):

        return json.dumps([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "신규 Invoice가 생성되었습니다.\n<@U086W2H95K4><@U07B2HY3E3F><@U036VMJAX2N><@U070KTKCD5L><@U06ECHJP7GV><@U05B5G8BK6C>"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"`PI 발행일` : {pi_request_date}\n`PI No` : {pi_no}\n`Export No` : {export_no}\n`Buyer Name` : {buyer_name}\n`Country` : {country}\n`Invoice Amount` : {summed_amount}\n"
                }
            },
            {
                "type": "divider"
            }
        ])

    @staticmethod
    def get_slack_new_buyer_post_block(corporate_name, business_name, country, url, mau, pic):

        return json.dumps([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "신규 B2B 업체가 추가되었어요 🤩"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ 법인명:* {corporate_name}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ 상호명:* {business_name}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ 국가:* {country}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ URL* : {url}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ MAU* : {mau}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*・ 담당자* : {pic}"
                }
            }
        ])

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
                    "text": f"*이퀄베리 US(NEW) {today} 실적 보고♡*"
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
                    "text": f"・ 금주 업로드 포스트수: *{this_week_posts}건*"
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
                    "text": f"・ 지난주 업로드 포스트수: *{last_week_posts}건*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"・ 지난주 업로드 뷰수 누적: *{last_week_play_count}회*"
                }
            }
        ])
